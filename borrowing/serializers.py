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
        print(validated_data)
        validated_data["user"] = self.context["request"].user
        validated_data["actual_return_date"] = None
        validated_data["borrow_date"] = datetime.date.today()
        book = validated_data["book"]
        if book.inventory == 0:
            raise serializers.ValidationError("Book is not available")
        if (
            validated_data["expected_return_date"]
            <= validated_data["borrow_date"]
        ):
            raise serializers.ValidationError(
                "Expected return date must be after borrow date."
            )
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

    def update(self, instance, validated_data):
        print(validated_data)
        if (
            validated_data["actual_return_date"]
            and validated_data["actual_return_date"] < instance.borrow_date
        ):
            raise serializers.ValidationError(
                "Actual return date must be on or after borrow date."
            )
        return super().update(instance, validated_data)


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
