import datetime
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


from book.models import Book
from borrowing.models import Borrowing
from user import serializers
from user.models import User

# Create your tests here.
BORROWING_URL = reverse("borrowing:borrowing-list")


def sample_book(**params):
    """Create and return a sample book"""
    defaults = {
        "title": "TestTitle",
        "author": "TestAuthor",
        "cover": "HARD",
        "inventory": 50,
        "daily_fee": Decimal("1.50"),
    }
    defaults.update(params)
    return Book.objects.create(**defaults)


def sample_borrowing(user: User, **params):
    """Create and return a sample borrowing"""
    book = sample_book()
    defaults = {
        "borrow_date": datetime.date.fromisocalendar(2025, 1, 1),
        "expected_return_date": datetime.date.fromisocalendar(2025, 10, 1),
        "actual_return_date": None,
        "book": book,
        "user": user,
    }
    defaults.update(params)
    return Borrowing.objects.create(**defaults)


class UnauthorizedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="TESTPASSWORD"
        )
        self.client.force_authenticate(self.user)

    def test_borrowing_list(self):
        sample_borrowing(user=self.user)
        sample_borrowing(user=self.user)

        borrowing = Borrowing.objects.all()
        res = self.client.get(BORROWING_URL)
        serializer = BorrowingListSerializer(borrowing, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_borrowing_list_filter_by_returned_status(self):
        borrowing1 = sample_borrowing(user=self.user)
        borrowing2 = sample_borrowing(
            user=self.user, actual_return_date=datetime.date.today()
        )

        serializer1 = BorrowingListSerializer(borrowing1)
        serializer2 = BorrowingListSerializer(borrowing2)
        for stat in ("true", "1", "yes"):
            res = self.client.get(BORROWING_URL, {"is_active": stat})

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIn(serializer1.data, res.data)
        for stat in ("false", "0", "no"):
            res = self.client.get(BORROWING_URL, {"is_active": stat})

            self.assertEqual(res.status_code, status.HTTP_200_OK)
            self.assertIn(serializer2.data, res.data)

    def test_borrowing_list_filter_by_user_id_forbidden(self):
        sample_borrowing(user=self.user)
        sample_borrowing(
            user=self.user, actual_return_date=datetime.date.today()
        )

        borrowings = Borrowing.objects.all()
        res = self.client.get(BORROWING_URL, {"user_id": 3})
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        for borrowing in serializer.data:
            self.assertEqual(borrowing.get("user"), self.user.email)

    def test_retrieve_borrowing_detail(self):
        borrowing = sample_borrowing(user=self.user)
        serializer = BorrowingDetailSerializer(borrowing)

        res = self.client.get(
            reverse("borrowing:borrowing-detail", args=[borrowing.id])
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_borrowing_success(self):
        book = sample_book()
        inv = book.inventory
        payload = {
            "expected_return_date": datetime.date.fromisocalendar(2025, 12, 5),
            "book": book.id,
        }
        res = self.client.post(BORROWING_URL, payload)

        created_borrowing = Borrowing.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_borrowing.book, book)
        self.assertEqual(created_borrowing.user, self.user)
        self.assertEqual(
            created_borrowing.borrow_date,
            datetime.date.today(),
        )
        self.assertEqual(created_borrowing.actual_return_date, None)
        self.assertEqual(created_borrowing.book.inventory, inv - 1)

    def test_delete_borrowing_forbidden(self):
        book = sample_borrowing(user=self.user)
        res = self.client.delete(reverse("book:books-detail", args=[book.id]))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class AdminUserBorrowingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="TESTPASSWORD", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_borrowing_list_filter_by_user_id(self):
        sample_borrowing(user=self.user)
        sample_borrowing(
            user=self.user, actual_return_date=datetime.date.today()
        )

        borrowings = Borrowing.objects.all()
        res = self.client.get(BORROWING_URL, {"user_id": 3})
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        for borrowing in serializer.data:
            self.assertEqual(borrowing.get("user"), self.user.email)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
