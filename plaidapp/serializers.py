from rest_framework import serializers
from .models import PlaidItem


class PlaidItemSerializer(serializers.ModelSerializer):
    """
    PlaidItem serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PlaidItem
        fields = ("id", "item_id", "access_token", "user", "institution_id", "institution_name")
        read_only_fields = ("id", "user")
