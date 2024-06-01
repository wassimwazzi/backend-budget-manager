from .models import PlaidItem, PlaidTransaction, PlaidAccount
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from .utils import client, pretty_print_response, format_error
import plaid


def sync_transactions(item_id):
    """
    Sync transactions for an item
    """

    def get_or_create_account(**kwargs):
        item = kwargs["item"]
        account_id = kwargs["account_id"]

    item = PlaidItem.objects.get(item_id=item_id)
    access_token = item.access_token
    cursor, added, modified, removed, has_more = "", [], [], [], True
    try:
        while has_more:
            request = TransactionsSyncRequest(access_token=access_token, cursor=cursor)
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
        # TODO: Save last cursor
        return {"added": added, "modified": modified, "removed": removed}
    except plaid.ApiException as e:
        return format_error(e)
