import datetime
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
        read_only_fields = ("id", "user")

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
