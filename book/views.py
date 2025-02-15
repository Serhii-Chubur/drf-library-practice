from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes

from book.models import Book
from book.permissions import IsAdminOrReadOnly
from book.serializers import BookListSerializer, BookSerializer


# Create your views here.
class CustomBoookPagination(PageNumberPagination):
    page_size = 5


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomBoookPagination

    def get_permissions(self):
        if self.action == "retrieve":
            return [
                IsAuthenticated(),
            ]
        return super().get_permissions()

    def get_queryset(self):
        is_available = self.request.GET.get("is_available")
        if is_available == "True":
            return self.queryset.filter(inventory__gt=0)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return super().get_serializer_class()

    @action(detail=False, url_path="is-available")
    def is_available(self, request, *args, **kwargs):
        """
        Returns a list of all books that
        are currently available in the library.

        Endpoint: books/?is_available=True
        """

        return HttpResponseRedirect(
            reverse("book:books-list") + "?is_available=True"
        )

    @action(
        detail=False,
        url_name="all",
        url_path="all-books",
    )
    def all_books(self, request, *args, **kwargs):
        """
        Redirects to the list of all books.

        Endpoint: book/all-books/
        """
        return HttpResponseRedirect(reverse("book:books-list"))

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                name="is_available",
                description="Filter by availability",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Returns a list of books.

        This method is used to retrieve a list of books based on the
        current queryset and any filters applied.

        It uses the parent class's list method to perform the action.
        """

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Returns a single book.

        This method is used to retrieve a single book based on the
        provided primary key.

        It uses the parent class's retrieve method to perform the action.
        """

        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="title", type=str, required=True),
            OpenApiParameter(name="author", type=str, required=True),
            OpenApiParameter(
                name="cover",
                type=str,
                examples=[
                    OpenApiExample(value="HARD", name="Hard"),
                    OpenApiExample(value="SOFT", name="Soft"),
                ],
                required=True,
            ),
            OpenApiParameter(name="inventory", type=str, required=True),
            OpenApiParameter(
                name="daily_fee", type=OpenApiTypes.DECIMAL, required=True
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        """
        Creates a new book.

        This method is used to create a new book based on the provided data.
        """

        return super().create(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="title", type=str, required=True),
            OpenApiParameter(name="author", type=str, required=True),
            OpenApiParameter(
                name="cover",
                type=str,
                examples=[
                    OpenApiExample(value="HARD", name="Hard"),
                    OpenApiExample(value="SOFT", name="Soft"),
                ],
                required=True,
            ),
            OpenApiParameter(name="inventory", type=str, required=True),
            OpenApiParameter(
                name="daily_fee", type=OpenApiTypes.DECIMAL, required=True
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        """
        Updates an existing book.

        This method is used to update an existing book based on the
        provided primary key and data.
        """

        return super().update(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(name="title", type=str, required=False),
            OpenApiParameter(name="author", type=str, required=False),
            OpenApiParameter(
                name="cover",
                type=str,
                examples=[
                    OpenApiExample(value="HARD", name="Hard"),
                    OpenApiExample(value="SOFT", name="Soft"),
                ],
                required=False,
            ),
            OpenApiParameter(name="inventory", type=str, required=False),
            OpenApiParameter(
                name="daily_fee", type=OpenApiTypes.DECIMAL, required=False
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an existing book.
        This method is used to update
        an existing book based on the provided primary key and data.
        """

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Deletes an existing book.

        Admin only.

        This method is used to delete an existing book based on the
        provided primary key.
        """

        return super().destroy(request, *args, **kwargs)
