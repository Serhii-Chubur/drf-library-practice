import datetime
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction


from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingReturnSerializer,
)


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


class BorrowingDetailAPIView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated,)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def return_book(request, pk, *args, **kwargs):
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
            return Response(borrowing_serializer.data)
        return Response(
            borrowing_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(borrowing_serializer.data)
