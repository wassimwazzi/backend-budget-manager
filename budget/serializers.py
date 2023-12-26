from rest_framework import serializers
from .models import Budget
from category.serializers import CategorySerializer


class BudgetSerializer(serializers.ModelSerializer):
    """
    Budget serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategorySerializer(read_only=True)
    start_date = serializers.DateField(
        input_formats=["%Y-%m", "%Y-%m-%d"], format="%Y-%m"
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    class Meta:
        model = Budget
        fields = ("id", "category", "amount", "currency", "start_date", "user")
        read_only_fields = ("id", "user")
