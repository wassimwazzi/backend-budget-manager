from rest_framework import serializers
from .models import Transaction
from category.serializers import CategorySerializer


class TransactionSerializer(serializers.ModelSerializer):
    """
    Transaction serializer
    """

    category = CategorySerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "code",
            "amount",
            "currency",
            "date",
            "description",
            "category",
            "inferred_category",
            "file",
            "user",
        )
        read_only_fields = ("id", "user", "inferred_category", "file")
