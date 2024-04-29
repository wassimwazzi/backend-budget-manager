from rest_framework import viewsets
from rest_framework import serializers
from django.conf import settings
from rest_framework.response import Response
from .serializers import PlaidItemSerializer
from .models import PlaidItem
from queryset_mixin import QuerysetMixin
from rest_framework.decorators import action

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from .utils import client


class PlaidItemView(QuerysetMixin, viewsets.ModelViewSet):
    serializer_class = PlaidItemSerializer

    def get_queryset(self):
        """
        This view should return a list of all the plaid items
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = PlaidItem.objects.filter(user=user)
        return self.get_filtered_queryet(queryset)

    @action(detail=False, methods=["post"])
    def create_link_token(self, request):
        """
        Create a link token for the user
        """
        print(settings.PLAID_ENV)
        # Get the client_user_id by searching for the current user
        user = request.user
        client_user_id = str(user.id)
        # Create a link_token for the given user
        request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="Budget Manager",
            country_codes=[CountryCode("CA"), CountryCode("US")],
            # redirect_uri=settings.PLAID_REDIRECT_URI,
            language="en",
            # webhook='https://webhook.example.com',
            user=LinkTokenCreateRequestUser(client_user_id=client_user_id),
        )
        response = client.link_token_create(request)
        return Response(response.to_dict())

    @action(detail=False, methods=["post"])
    def exchange_public_token(self, request):
        """
        Exchange a public token for an access token
        """
        public_token = request.data.get("public_token")
        print("wawawaw")
        print(public_token)
        user = request.user
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        access_token = response["access_token"]
        item_id = response["item_id"]
        # Check if the item already exists
        if PlaidItem.objects.filter(item_id=item_id, user=user).exists():
            item = PlaidItem.objects.get(item_id=item_id, user=user)
            return Response(PlaidItemSerializer(item).data)
        item = PlaidItem.objects.create(
            user=user,
            access_token=access_token,
            item_id=item_id,
        )
        return Response(PlaidItemSerializer(item).data)
