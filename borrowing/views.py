import datetime
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)

from notification_system.library_bot import send_returned_message


# Create your views here.
class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.GET.get("user_id")
        is_active = self.request.GET.get("is_active")
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        if is_active:
            if is_active.lower() in ("true", "1", "yes"):
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() in ("false", "0", "no"):
                queryset = queryset.filter(actual_return_date__isnull=False)

        if self.request.user.is_superuser:
            if user_id:
                queryset = queryset.filter(user__id=user_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BorrowingListSerializer
        return super().get_serializer_class()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="expected_return_date",
                type=OpenApiTypes.DATE,
                required=True,
            ),
            OpenApiParameter(name="book_id", type=int, required=True),
        ]
    )
    def post(self, request, *args, **kwargs):
        """
        Creates a new borrowing.

        This method is used to create a new borrowing based on the
        provided expected return date and book id.
        """
        return super().post(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                type=str,
                required=False,
            ),
            OpenApiParameter(name="user_id", type=str, required=False),
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Returns a list of borrowings.

        This method is used to retrieve a list of borrowings based on the
        current queryset and any filters applied.

        It uses the parent class's get method to perform the action.

        Parameters:\n
            is_active (str): Filter borrowings
            by whether they are active or not.
            Values: "false", "0", "no", "true", "1", "yes"\n
            user_id (int): Filter borrowings
            by the user who borrowed the book. Admin only parameter
        """
        return super().get(request, *args, **kwargs)


class BorrowingDetailAPIView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        """
        Retrieves the details of a specific borrowing.

        This method is used to retrieve
        the borrowing details based on the
        provided primary key in the URL.
        """

        return super().get(request, *args, **kwargs)


@extend_schema(
    request=BorrowingReturnSerializer, responses=BorrowingReturnSerializer
)
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def return_book(request, pk, *args, **kwargs):
    """
    Returns the borrowing with given pk.
    If the borrowing is not found, returns HTTP 404.
    If the borrowing is already returned,
    returns HTTP 400 with message "Book is already returned".
    If the request method is PUT,
    returns the borrowing with the actual return date set to today.
    If the PUT request is successful,
    sends a message to the user that the book has been returned.
    """

    try:
        borrowing = Borrowing.objects.get(pk=pk)
        book = borrowing.book
    except borrowing.DoesNotExist:
        return Response(
            {"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND
        )

    borrowing_serializer = BorrowingDetailSerializer(borrowing)

    if request.method == "GET":
        if borrowing.actual_return_date:
            return Response(
                {"message": "Book is already returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(borrowing_serializer.data)

    if request.method == "PUT":

        borrowing_serializer = BorrowingReturnSerializer(
            borrowing,
            data={
                "actual_return_date": datetime.date.today(),
            },
        )

        if borrowing_serializer.is_valid():
            with transaction.atomic():
                borrowing_serializer.save()
                book.inventory += 1
                book.save()
                send_returned_message(request.user, book, borrowing)
            return Response(borrowing_serializer.data)
        return Response(
            borrowing_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(borrowing_serializer.data)
