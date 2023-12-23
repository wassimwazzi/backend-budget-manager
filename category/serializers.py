from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        model = Category
        fields = ("id", "category", "income", "description", "user")
        read_only_fields = ("id", "user")
