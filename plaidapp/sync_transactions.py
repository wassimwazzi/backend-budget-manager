from .models import (
    PlaidItem,
    PlaidTransaction,
    PlaidAccount,
    PlaidItemSync,
    Location,
    TransactionStatus,
)
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from .utils import client, pretty_print_response, format_error
import plaid
from django.utils import timezone
from django.db import transaction as db_transaction
from transaction.models import Transaction
from currency.models import Currency
from category.models import Category
from inference.text_classifier import fuzzy_search


def get_more_data(access_token, cursor):
    request = TransactionsSyncRequest(access_token=access_token, cursor=cursor)
    response = client.transactions_sync(request).to_dict()
    cursor = response["next_cursor"]
    has_more = response["has_more"]
    # # Add this page of results
    added = response["added"]
    modified = response["modified"]
    removed = response["removed"]
    accounts = response["accounts"]
    return cursor, has_more, accounts, added, modified, removed


def save_cursor(item, cursor):
    """
    Save the cursor for a PlaidItem.
    Create the PlaidItemSync object if it doesn't exist.
    """
    item_sync = PlaidItemSync.objects.get_or_create(
        item=item, defaults={"last_synced": timezone.now()}
    )[0]
    item_sync.cursor = cursor
    item_sync.last_synced = timezone.now()
    item_sync.save()


def create_accounts(item, accounts):
    """
    Create or update PlaidAccount objects.
    """
    for account_json in accounts:
        account = PlaidAccount.objects.get_or_create(
            item=item, account_id=account_json["account_id"]
        )[0]
        account.mask = account_json["mask"]
        account.name = account_json["name"]
        account.official_name = account_json.get("official_name")
        account.subtype = account_json.get("subtype")
        account.type = account_json["type"]
        account.iso_currency_code = account_json.get("iso_currency_code")
        account.available_balance = account_json.get("available_balance")
        account.current_balance = account_json.get("current_balance")
        account.limit = account_json.get("limit")
        account.save()


def get_category(item, transaction):
    user = item.user
    amount = float(transaction["amount"])
    if amount > 0:  # expense
        categories = Category.objects.filter(user=user, income=False)
    else:  # income
        categories = Category.objects.filter(user=user, income=True)
    for plaid_category in transaction["category"]:
        category = fuzzy_search(
            plaid_category, categories.values_list("category", flat=True)
        )
        if category:
            return Category.objects.get(category=category, user=user)
    return categories.get(is_default=True)


def add_transactions(item, transactions):
    """
    Create PlaidTransaction objects.
    """
    for plaid_trans in transactions:
        account = PlaidAccount.objects.get(
            item=item, account_id=plaid_trans["account_id"]
        )
        location = Location.objects.get_or_create(
            city=plaid_trans.get("city"),
            region=plaid_trans.get("region"),
            postal_code=plaid_trans.get("postal_code"),
            country=plaid_trans.get("country"),
            address=plaid_trans.get("address"),
        )[0]
        location.save()
        plaid_transaction = PlaidTransaction.objects.create(
            item=item,
            account=account,
            plaid_transaction_id=plaid_trans.get("transaction_id"),
            category_id=plaid_trans.get("category_id"),
            category=plaid_trans.get("category"),
            pending=plaid_trans.get("pending"),
            location=location,
            name=plaid_trans.get("merchant_name"),
            status=TransactionStatus.ADDED,
        )
        plaid_transaction.save()

        transaction = Transaction.objects.create(
            code=plaid_trans["transaction_code"],
            amount=abs(float(plaid_trans["amount"])),
            currency=Currency.objects.get_or_create(
                code=plaid_trans["iso_currency_code"]
            )[0],
            date=plaid_trans["date"],
            description=plaid_trans["name"],
            category=get_category(item, plaid_trans),
            plaid_transaction=plaid_transaction,
            user=item.user,
        )
        transaction.save()


def sync_transactions(item_id):
    """
    Sync transactions for an item
    """
    # TODO handle errors like item does not exist
    # TODO set max lookback days
    item = PlaidItem.objects.get(item_id=item_id)
    access_token = item.access_token
    cursor, has_more = "", True
    try:
        with db_transaction.atomic():
            while has_more:
                cursor, has_more, accounts, added, modified, removed = get_more_data(
                    access_token, cursor
                )
                create_accounts(item, accounts)
                add_transactions(item, added)
            save_cursor(item, cursor)
            return {"added": added, "modified": modified, "removed": removed}
    except plaid.ApiException as e:
        return format_error(e)
