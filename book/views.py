from rest_framework import viewsets

from book.models import Book
from book.serializers import BookSerializer


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        pass

    def get_serializer_class(self):
        pass


# - POST:        books/           - add new
# - GET:         books/           - get a list of books
# - GET:         books/\<id\>/      - get book detail info
# - PUT/PATCH:   books/\<id\>/      - update book
# - DELETE:      books/\<id\>/      - delete book
