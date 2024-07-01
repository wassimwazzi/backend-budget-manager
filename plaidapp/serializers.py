from rest_framework import serializers
from .models import PlaidItem, PlaidItemSync, PlaidAccount, PlaidTransaction, Location
import json


class PlaidItemSerializer(serializers.ModelSerializer):
    """
    PlaidItem serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PlaidItem
        fields = "__all__"
        read_only_fields = ("id", "user")


class PlaidItemSyncSerializer(serializers.ModelSerializer):
    """
    PlaidItemSync serializer
    """

    item = PlaidItemSerializer()

    class Meta:
        model = PlaidItemSync
        fields = "__all__"
        # read_only_fields = "__all__"


class PlaidAccountSerializer(serializers.ModelSerializer):
    """
    PlaidAccount serializer
    """

    class Meta:
        model = PlaidAccount
        fields = "__all__"
        # read_only_fields = "__all__"


class PlaidLocationSerializer(serializers.ModelSerializer):
    """
    PlaidLocation serializer
    """

    class Meta:
        model = Location
        fields = "__all__"
        # read_only_fields = "__all__"


class CategoryField(serializers.Field):
    """
    Custom field to handle category list.
    Since the category field is a list of strings, we need to serialize it as a JSON string.
    """

    def to_representation(self, value):
        try:
            return json.loads(value) if value else []
        except json.JSONDecodeError:
            return value

    def to_internal_value(self, data):
        return json.dumps(data)


class PlaidTransactionSerializer(serializers.ModelSerializer):
    """
    PlaidTransaction serializer
    """

    location = PlaidLocationSerializer()
    account = PlaidAccountSerializer()
    item_sync = PlaidItemSyncSerializer()
    category = CategoryField()

    class Meta:
        model = PlaidTransaction
        fields = "__all__"
        # read_only_fields = "__all__"
