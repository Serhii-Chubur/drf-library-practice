from decimal import Decimal

# from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APIClient

from book.serializers import BookListSerializer, BookSerializer


from book.models import Book

# Create your tests here.
BOOK_URL = reverse("book:books-list")


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


class UnauthorizedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        book = sample_book()
        res = self.client.get(reverse("book:books-detail", args=[book.id]))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="TESTPASSWORD"
        )
        self.client.force_authenticate(self.user)

    def test_book_list(self):
        sample_book()
        sample_book(title="Another Book", author="Another Author")

        books = Book.objects.all()
        res = self.client.get(BOOK_URL)
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_book_list_filter_by_availability(self):
        book1 = sample_book()
        book2 = sample_book(
            title="Another Book", author="Another Author", inventory=0
        )

        serializer1 = BookListSerializer(book1)
        serializer2 = BookListSerializer(book2)
        res = self.client.get(BOOK_URL, {"is_available": "True"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_all_books_redirects_to_book_list(self):
        url = reverse("book:books-all")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(res, reverse("book:books-list"))

    def test_retrieve_book_detail(self):
        book = sample_book()
        serializer = BookSerializer(book)

        res = self.client.get(reverse("book:books-detail", args=[book.id]))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_forbidden(self):
        payload = {
            "title": "BookTitle",
            "author": "BookAuthor",
            "cover": "SOFT",
            "inventory": 50,
            "daily_fee": Decimal("1.50"),
        }
        res = self.client.post(BOOK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_forbidden(self):
        book = sample_book()
        res = self.client.delete(reverse("book:books-detail", args=[book.id]))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminUserBookApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="TESTPASSWORD", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_book(self):
        payload = {
            "title": "BookTitle",
            "author": "BookAuthor",
            "cover": "SOFT",
            "inventory": 50,
            "daily_fee": Decimal("1.50"),
        }
        res = self.client.post(BOOK_URL, payload)

        books = Book.objects.all()
        book = Book.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(books.count(), 1)
        self.assertEqual(book.title, payload["title"])
        self.assertEqual(book.author, payload["author"])
        self.assertEqual(book.cover, payload["cover"])
        self.assertEqual(book.inventory, payload["inventory"])
        self.assertEqual(book.daily_fee, payload["daily_fee"])

    def test_delete_book(self):
        book = sample_book()
        res = self.client.delete(reverse("book:books-detail", args=[book.id]))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
