from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book", "user")
        read_only_fields = ("id", "actual_return_date")


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(read_only=True, slug_field="title")
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book")
        read_only_fields = ("id", "actual_return_date")


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = Borrowing
        fields = ("id", "borrow_date", "expected_return_date", "actual_return_date", "book")
        read_only_fields = ("id", "actual_return_date")
