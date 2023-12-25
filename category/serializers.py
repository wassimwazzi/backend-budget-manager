from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        model = Category
        fields = ("id", "category", "income", "description", "user", "is_default")
        read_only_fields = ("id", "user", "is_default")
