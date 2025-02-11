import datetime
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


# Create your views here.
class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.GET.get("user_id")
        is_active = self.request.GET.get("is_active")
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if is_active:
            if is_active.lower() in ("true", "1", "yes"):
                queryset = queryset.filter(actual_return_date__isnull=True)
            elif is_active.lower() in ("false", "0", "no"):
                queryset = queryset.filter(actual_return_date__isnull=False)
        return queryset


class BorrowingDetailAPIView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


@api_view(["GET", "PUT"])
def return_book(request, pk, *args, **kwargs):
    try:
        borrowing = Borrowing.objects.get(pk=pk)
        book = borrowing.book
    except borrowing.DoesNotExist:
        return Response(
            {"message": "Book not found"}, status=status.HTTP_404_NOT_FOUND
        )

    borrowing_serializer = BorrowingSerializer(borrowing)

    if request.method == "GET":
        if borrowing.actual_return_date:
            return Response(
                {"message": "Book is already returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(borrowing_serializer.data)

    if request.method == "PUT":

        borrowing_serializer = BorrowingSerializer(
            borrowing,
            data={
                "book": book.id,
                "expected_return_date": borrowing.expected_return_date,
                "actual_return_date": datetime.date.today(),
            },
        )

        if borrowing_serializer.is_valid():
            with transaction.atomic():
                borrowing_serializer.save()
                book.inventory += 1
                book.save()
            return Response(borrowing_serializer.data)
        return Response(
            borrowing_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(borrowing_serializer.data)
