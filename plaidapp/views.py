from rest_framework import viewsets
from django.conf import settings
from rest_framework.response import Response
from .serializers import PlaidItemSerializer, PlaidTransactionSerializer
from .models import PlaidItem, PlaidTransaction, PlaidAccount, PlaidItemSync
from queryset_mixin import QuerysetMixin
from rest_framework.decorators import action

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest,
)
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_sync_request import TransactionsSyncRequest
import plaid
from .utils import client, pretty_print_response, format_error
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

COUNTRY_CODES = [CountryCode("CA"), CountryCode("US")]


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
        # Get the client_user_id by searching for the current user
        user = request.user
        client_user_id = str(user.id)
        # Create a link_token for the given user
        request = LinkTokenCreateRequest(
            products=[Products("auth"), Products("transactions")],
            client_name="Budget Manager",
            country_codes=COUNTRY_CODES,
            # redirect_uri=settings.PLAID_REDIRECT_URI,
            language="en",
            webhook=settings.PLAID_WEBHOOK_URL,
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
        user = request.user
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = client.item_public_token_exchange(request)
        access_token = response["access_token"]
        item_id = response["item_id"]
        # Check if the item already exists
        if PlaidItem.objects.filter(item_id=item_id, user=user).exists():
            item = PlaidItem.objects.get(item_id=item_id, user=user)
            return Response(PlaidItemSerializer(item).data)
        item_request = ItemGetRequest(access_token=access_token)
        item_response = client.item_get(item_request)
        institution_id = item_response["item"]["institution_id"]
        institution_request = InstitutionsGetByIdRequest(
            institution_id,
            country_codes=COUNTRY_CODES,
        )
        institution_response = client.institutions_get_by_id(institution_request)
        institution_name = institution_response["institution"]["name"]
        item = PlaidItem.objects.create(
            user=user,
            access_token=access_token,
            item_id=item_id,
            institution_id=institution_id,
            institution_name=institution_name,
        )
        return Response(PlaidItemSerializer(item).data)


class PlaidTransactionView(QuerysetMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PlaidTransactionSerializer

    def get_queryset(self):
        """
        This view should return a list of all the transactions
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = PlaidTransaction.objects.filter(account__item__user=user)
        return self.get_filtered_queryet(queryset)

    @action(detail=False, methods=["post"])
    def sync(self, request):
        """
        Sync transactions for an item
        """

        def get_or_create_account(**kwargs):
            item = kwargs["item"]
            account_id = kwargs["account_id"]

        item_id = request.data.get("item_id")
        user = request.user
        item = PlaidItem.objects.get(item_id=item_id, user=user)
        access_token = item.access_token
        cursor, added, modified, removed, has_more = "", [], [], [], True
        try:
            while has_more:
                request = TransactionsSyncRequest(
                    access_token=access_token, cursor=cursor
                )
                response = client.transactions_sync(request).to_dict()
                cursor = response["next_cursor"]
                has_more = response["has_more"]
                # # Add this page of results
                added.extend(response["added"])
                modified.extend(response["modified"])
                removed.extend(response["removed"])
                # has_more = response["has_more"]
                # # Update cursor to the next cursor
                # for t in response["transactions"]:
                #     account = PlaidAccount.objects.get(account_id=t["account_id"])
                #     transaction = PlaidTransaction.objects.create(
                #         account=account,
                #         transaction_id=t["transaction_id"],
                #         account_owner=t["account_owner"],
                #         amount=t["amount"],
                #         iso_currency_code=t["iso_currency_code"],
                #         unofficial_currency_code=t[
                #             "unofficial_currency_code"
                #         ],
                #         category=t["category"],
                #         category_id=t["category_id"],
                #         date=t["date"],
                #         location=t["location"],
                #         name=t["name"],
                #         payment_channel=t["payment_channel"],
                #         pending=t["pending"],
                #         pending_transaction_id=t[
                #             "pending_transaction_id"
                #         ],
                #         transaction_code=t["transaction_code"],
                #         transaction_type=t["transaction_type"],
                #     )
                pretty_print_response(response)
            return Response({"added": added, "modified": modified, "removed": removed})
        except plaid.ApiException as e:
            return Response(format_error(e))
