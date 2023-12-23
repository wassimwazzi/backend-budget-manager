from rest_framework import serializers
from .models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    """
    Currency serializer
    """

    class Meta:
        model = Currency
        fields = ["code"]
