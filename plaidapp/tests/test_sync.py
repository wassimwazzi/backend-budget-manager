import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from transaction.tests.factories import TransactionFactory
from transaction.models import Transaction
from unittest.mock import patch
from ..sync_transactions import sync_transactions
from ..models import PlaidTransaction, PlaidAccount
from .factories import (
    PlaidAccountFactory,
    PlaidItemFactory,
    PlaidTransactionFactory,
)


# Decorator for mocking the get_more_data function
def get_more_data_mock(
    cursor=None, has_more=False, accounts=None, added=None, modified=None, removed=None
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with patch("plaidapp.sync_transactions.get_more_data") as mock:
                mock.return_value = cursor, has_more, accounts, added, modified, removed
                func(*args, **kwargs)

        return wrapper

    return decorator


MOCK_PLAID_ACCOUNT = {
    "account_id": "BxBXxLj1m4HMXBm9WZZmCWVbPjX16EHwv99vp",
    "balances": {
        "available": 110.94,
        "current": 110.94,
        "iso_currency_code": "USD",
        "limit": None,
        "unofficial_currency_code": None,
    },
    "mask": "0000",
    "name": "Plaid Checking",
    "official_name": "Plaid Gold Standard 0% Interest Checking",
    "subtype": "checking",
    "type": "depository",
}

MOCK_PLAID_ADDED_TRANSACTION = {
    "account_id": "BxBXxLj1m4HMXBm9WZZmCWVbPjX16EHwv99vp",
    "account_owner": None,
    "amount": 72.1,
    "iso_currency_code": "USD",
    "unofficial_currency_code": None,
    "category": ["Shops", "Supermarkets and Groceries"],
    "category_id": "19046000",
    "check_number": None,
    "counterparties": [
        {
            "name": "Walmart",
            "type": "merchant",
            "logo_url": "https://plaid-merchant-logos.plaid.com/walmart_1100.png",
            "website": "walmart.com",
            "entity_id": "O5W5j4dN9OR3E6ypQmjdkWZZRoXEzVMz2ByWM",
            "confidence_level": "VERY_HIGH",
        }
    ],
    "date": datetime.datetime.strptime("2023-09-24", "%Y-%m-%d").date(),
    "datetime": "2023-09-24T11:01:01Z",
    "authorized_date": "2023-09-22",
    "authorized_datetime": "2023-09-22T10:34:50Z",
    "location": {
        "address": "13425 Community Rd",
        "city": "Poway",
        "region": "CA",
        "postal_code": "92064",
        "country": "US",
        "lat": 32.959068,
        "lon": -117.037666,
        "store_number": "1700",
    },
    "name": "PURCHASE WM SUPERCENTER #1700",
    "merchant_name": "Walmart",
    "merchant_entity_id": "O5W5j4dN9OR3E6ypQmjdkWZZRoXEzVMz2ByWM",
    "logo_url": "https://plaid-merchant-logos.plaid.com/walmart_1100.png",
    "website": "walmart.com",
    "payment_meta": {
        "by_order_of": None,
        "payee": None,
        "payer": None,
        "payment_method": None,
        "payment_processor": None,
        "ppd_id": None,
        "reason": None,
        "reference_number": None,
    },
    "payment_channel": "in store",
    "pending": False,
    "pending_transaction_id": "no86Eox18VHMvaOVL7gPUM9ap3aR1LsAVZ5nc",
    "personal_finance_category": {
        "primary": "GENERAL_MERCHANDISE",
        "detailed": "GENERAL_MERCHANDISE_SUPERSTORES",
        "confidence_level": "VERY_HIGH",
    },
    "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_GENERAL_MERCHANDISE.png",
    "transaction_id": "lPNjeW1nR6CDn5okmGQ6hEpMo4lLNoSrzqDje",
    "transaction_code": None,
    "transaction_type": "place",
}

MOCK_PLAID_MODIFIED_TRANSACTION = {
    "account_id": "BxBXxLj1m4HMXBm9WZZmCWVbPjX16EHwv99vp",
    "account_owner": None,
    "amount": 28.34,
    "iso_currency_code": "USD",
    "unofficial_currency_code": None,
    "category": ["Food and Drink", "Restaurants", "Fast Food"],
    "category_id": "13005032",
    "check_number": None,
    "counterparties": [
        {
            "name": "DoorDash",
            "type": "marketplace",
            "logo_url": "https://plaid-counterparty-logos.plaid.com/doordash_1.png",
            "website": "doordash.com",
            "entity_id": "YNRJg5o2djJLv52nBA1Yn1KpL858egYVo4dpm",
            "confidence_level": "HIGH",
        },
        {
            "name": "Burger King",
            "type": "merchant",
            "logo_url": "https://plaid-merchant-logos.plaid.com/burger_king_155.png",
            "website": "burgerking.com",
            "entity_id": "mVrw538wamwdm22mK8jqpp7qd5br0eeV9o4a1",
            "confidence_level": "VERY_HIGH",
        },
    ],
    "date": datetime.datetime.strptime("2023-09-28", "%Y-%m-%d").date(),
    "datetime": "2023-09-28T15:10:09Z",
    "authorized_date": "2023-09-27",
    "authorized_datetime": "2023-09-27T08:01:58Z",
    "location": {
        "address": None,
        "city": None,
        "region": None,
        "postal_code": None,
        "country": None,
        "lat": None,
        "lon": None,
        "store_number": None,
    },
    "name": "Dd Doordash Burgerkin",
    "merchant_name": "Burger King",
    "merchant_entity_id": "mVrw538wamwdm22mK8jqpp7qd5br0eeV9o4a1",
    "logo_url": "https://plaid-merchant-logos.plaid.com/burger_king_155.png",
    "website": "burgerking.com",
    "payment_meta": {
        "by_order_of": None,
        "payee": None,
        "payer": None,
        "payment_method": None,
        "payment_processor": None,
        "ppd_id": None,
        "reason": None,
        "reference_number": None,
    },
    "payment_channel": "online",
    "pending": True,
    "pending_transaction_id": None,
    "personal_finance_category": {
        "primary": "FOOD_AND_DRINK",
        "detailed": "FOOD_AND_DRINK_FAST_FOOD",
        "confidence_level": "VERY_HIGH",
    },
    "personal_finance_category_icon_url": "https://plaid-category-icons.plaid.com/PFC_FOOD_AND_DRINK.png",
    "transaction_id": "yhnUVvtcGGcCKU0bcz8PDQr5ZUxUXebUvbKC0",
    "transaction_code": None,
    "transaction_type": "digital",
}

MOCK_PLAID_REMOVED_TRANSACTION = {
    "account_id": "BxBXxLj1m4HMXBm9WZZmCWVbPjX16EHwv99vp",
    "transaction_id": "CmdQTNgems8BT1B7ibkoUXVPyAeehT3Tmzk0l",
}
MOCK_NEXT_CURSOR = "tVUUL15lYQN5rBnfDIc1I8xudpGdIlw9nsgeXWvhOfkECvUeR663i3Dt1uf/94S8ASkitgLcIiOSqNwzzp+bh89kirazha5vuZHBb2ZA5NtCDkkV"
MOCK_SYNC_RESPONSE = {
    "accounts": [MOCK_PLAID_ACCOUNT],
    "added": [MOCK_PLAID_ADDED_TRANSACTION],
    "modified": [MOCK_PLAID_MODIFIED_TRANSACTION],
    "removed": [MOCK_PLAID_REMOVED_TRANSACTION],
    "next_cursor": MOCK_NEXT_CURSOR,
    "has_more": False,
    "request_id": "Wvhy9PZHQLV8njG",
    "transactions_update_status": "HISTORICAL_UPDATE_COMPLETE",
}


class TestSync(TestCase):
    def setUp(self) -> None:
        self.plaid_item = PlaidItemFactory()

    @get_more_data_mock(
        cursor=MOCK_NEXT_CURSOR,
        has_more=False,
        accounts=[MOCK_PLAID_ACCOUNT],
        added=[MOCK_PLAID_ADDED_TRANSACTION],
        modified=[],
        removed=[],
    )
    def test_adds_transaction(self):
        """
        Test that a transaction is added when a PlaidTransaction is added
        """
        sync_transactions(self.plaid_item.item_id)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(PlaidTransaction.objects.count(), 1)
        self.assertEqual(PlaidAccount.objects.count(), 1)

        transaction = Transaction.objects.first()
        plaid_transaction = PlaidTransaction.objects.first()
        account = PlaidAccount.objects.first()

        self.assertEqual(transaction.plaid_transaction, plaid_transaction)
        self.assertEqual(
            float(transaction.amount), MOCK_PLAID_ADDED_TRANSACTION["amount"]
        )
        self.assertEqual(
            transaction.currency.code, MOCK_PLAID_ADDED_TRANSACTION["iso_currency_code"]
        )
        self.assertEqual(transaction.date, MOCK_PLAID_ADDED_TRANSACTION["date"])
        self.assertEqual(
            transaction.description, MOCK_PLAID_ADDED_TRANSACTION["merchant_name"]
        )
        self.assertEqual(transaction.code, MOCK_PLAID_ADDED_TRANSACTION["name"])
        self.assertEqual(transaction.inferred_category, True)
        self.assertEqual(transaction.plaid_transaction, plaid_transaction)
        self.assertEqual(transaction.user, self.plaid_item.user)

        self.assertEqual(plaid_transaction.account, account)
        self.assertEqual(
            plaid_transaction.plaid_transaction_id,
            MOCK_PLAID_ADDED_TRANSACTION["transaction_id"],
        )
        self.assertEqual(
            plaid_transaction.category, str(MOCK_PLAID_ADDED_TRANSACTION["category"])
        )
        self.assertEqual(
            plaid_transaction.category_id, MOCK_PLAID_ADDED_TRANSACTION["category_id"]
        )
        self.assertEqual(
            plaid_transaction.location.address,
            MOCK_PLAID_ADDED_TRANSACTION["location"]["address"],
        )
        self.assertEqual(
            plaid_transaction.location.city,
            MOCK_PLAID_ADDED_TRANSACTION["location"]["city"],
        )
        self.assertEqual(
            plaid_transaction.location.region,
            MOCK_PLAID_ADDED_TRANSACTION["location"]["region"],
        )
        self.assertEqual(
            plaid_transaction.location.postal_code,
            MOCK_PLAID_ADDED_TRANSACTION["location"]["postal_code"],
        )
        self.assertEqual(
            plaid_transaction.location.country,
            MOCK_PLAID_ADDED_TRANSACTION["location"]["country"],
        )

    @get_more_data_mock(
        cursor=MOCK_NEXT_CURSOR,
        has_more=False,
        accounts=[MOCK_PLAID_ACCOUNT],
        added=[],
        modified=[],
        removed=[MOCK_PLAID_REMOVED_TRANSACTION],
    )
    def test_removes_transactions(self):
        """
        Test that a transaction is removed when a PlaidTransaction is removed
        """
        plaid_transaction = PlaidTransactionFactory(
            item_sync__item=self.plaid_item,
            plaid_transaction_id=MOCK_PLAID_REMOVED_TRANSACTION["transaction_id"],
        )
        transaction = TransactionFactory(plaid_transaction=plaid_transaction)
        sync_transactions(self.plaid_item.item_id)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(PlaidTransaction.objects.count(), 1)

        with self.assertRaises(ObjectDoesNotExist):
            Transaction.objects.get(pk=transaction.pk)

        plaid_transaction.refresh_from_db()
        self.assertEqual(plaid_transaction.status, "REMOVED")

    @get_more_data_mock(
        cursor=MOCK_NEXT_CURSOR,
        has_more=False,
        accounts=[MOCK_PLAID_ACCOUNT],
        added=[],
        modified=[MOCK_PLAID_MODIFIED_TRANSACTION],
        removed=[],
    )
    def test_modifies_transactions(self):
        """
        Test that a transaction is modified when a PlaidTransaction is modified
        """
        plaid_transaction = PlaidTransactionFactory(
            item_sync__item=self.plaid_item,
            plaid_transaction_id=MOCK_PLAID_MODIFIED_TRANSACTION["transaction_id"],
        )
        transaction = TransactionFactory(plaid_transaction=plaid_transaction)
        sync_transactions(self.plaid_item.item_id)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(PlaidTransaction.objects.count(), 1)

        transaction.refresh_from_db()
        self.assertEqual(
            float(transaction.amount), MOCK_PLAID_MODIFIED_TRANSACTION["amount"]
        )
        self.assertEqual(
            transaction.currency.code,
            MOCK_PLAID_MODIFIED_TRANSACTION["iso_currency_code"],
        )
        self.assertEqual(transaction.date, MOCK_PLAID_MODIFIED_TRANSACTION["date"])
        self.assertEqual(
            transaction.description, MOCK_PLAID_MODIFIED_TRANSACTION["merchant_name"]
        )
        self.assertEqual(transaction.code, MOCK_PLAID_MODIFIED_TRANSACTION["name"])
        self.assertEqual(transaction.inferred_category, True)
        self.assertEqual(transaction.plaid_transaction, plaid_transaction)
        self.assertEqual(transaction.user, self.plaid_item.user)

        plaid_transaction.refresh_from_db()
        self.assertEqual(
            plaid_transaction.category, str(MOCK_PLAID_MODIFIED_TRANSACTION["category"])
        )
        self.assertEqual(
            plaid_transaction.category_id,
            MOCK_PLAID_MODIFIED_TRANSACTION["category_id"],
        )

    @get_more_data_mock(
        cursor=MOCK_NEXT_CURSOR,
        has_more=False,
        accounts=[MOCK_PLAID_ACCOUNT],
        added=[MOCK_PLAID_ADDED_TRANSACTION],
        modified=[],
        removed=[],
    )
    def test_max_lookback_date(self):
        """
        Does not create transactions older than the max lookback date
        """
        transaction_date = MOCK_PLAID_ADDED_TRANSACTION["date"]
        self.plaid_item.max_lookback_date = transaction_date + datetime.timedelta(
            days=1
        )
        self.plaid_item.save()
        sync_transactions(self.plaid_item.item_id)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(PlaidTransaction.objects.count(), 0)

    @get_more_data_mock(
        cursor=MOCK_NEXT_CURSOR,
        has_more=False,
        accounts=[MOCK_PLAID_ACCOUNT],
        added=[],
        modified=[MOCK_PLAID_MODIFIED_TRANSACTION],
        removed=[],
    )
    def test_modify_does_not_modify_before_lookback_date(self):
        """
        Does not modify transactions older than the max lookback date
        """
        transaction_date = MOCK_PLAID_MODIFIED_TRANSACTION["date"]
        self.plaid_item.max_lookback_date = transaction_date + datetime.timedelta(
            days=1
        )
        self.plaid_item.save()
        # raises error if transaction is not found
        sync_transactions(self.plaid_item.item_id)
        self.assertEqual(Transaction.objects.count(), 0)


    @get_more_data_mock(
        cursor=MOCK_NEXT_CURSOR,
        has_more=False,
        accounts=[MOCK_PLAID_ACCOUNT],
        added=[],
        modified=[MOCK_PLAID_MODIFIED_TRANSACTION],
        removed=[],
    )
    def test_when_modified_transaction_does_not_exist(self):
        """
        Does not modify transactions that do not exist
        Should not raise error
        """
        sync_transactions(self.plaid_item.item_id)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(PlaidTransaction.objects.count(), 0)