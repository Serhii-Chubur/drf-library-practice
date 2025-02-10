from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import action

from book.models import Book
from book.serializers import BookListSerializer, BookSerializer


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        is_available = self.request.GET.get("is_available")
        if is_available == "True":
            return self.queryset.filter(inventory__gt=0)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return super().get_serializer_class()

    @action(detail=False)
    def is_available(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            reverse("book:books-list") + "?is_available=True"
        )

    @action(detail=False)
    def all_books(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("book:books-list"))
