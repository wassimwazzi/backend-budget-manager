from rest_framework import serializers
from .models import Transaction
from category.serializers import CategorySerializer
from plaidapp.serializers import PlaidTransactionSerializer
from django.utils import timezone


class TransactionSerializer(serializers.ModelSerializer):
    """
    Transaction serializer
    """

    category = CategorySerializer(read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    plaid_transaction = PlaidTransactionSerializer(read_only=True)

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
            "plaid_transaction",
        )
        read_only_fields = ("id", "user", "inferred_category", "file")

    def validate_amount(self, value):
        """
        Validate amount
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be larger than 0")
        return value

    def validate_category(self, value):
        """
        Validate category
        """
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("Invalid category")
        return value

    def validate_date(self, value):
        """
        Validate date
        """
        if isinstance(value, str):
            value = timezone.datetime.strptime(self.date, "%Y-%m-%d").date()
        if value > timezone.now().date():
            raise serializers.ValidationError("Date cannot be in the future")
        return value

    def validate(self, data):
        """
        Validate transaction
        """
        if not data.get("code", None) and not data.get("description", None):
            raise serializers.ValidationError(
                "Code and description cannot both be null"
            )
        return data
