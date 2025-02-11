import datetime
from book.serializers import BookSerializer, BookListSerializer
from borrowing.models import Borrowing
from rest_framework import serializers


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("id", "user", "actual_return_date")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["actual_return_date"] = None
        validated_data["borrow_date"] = datetime.date.today()
        book = validated_data["book"]
        if book.inventory == 0:
            raise serializers.ValidationError("Book is not available")
        book.inventory -= 1
        book.save()
        return super().create(validated_data)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "book",
            "user",
            "actual_return_date",
        )
        read_only_fields = (
            "id",
            "borrow_date",
            "book",
            "user",
        )


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookListSerializer()
    user = serializers.StringRelatedField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "book",
            "user",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = serializers.StringRelatedField()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
