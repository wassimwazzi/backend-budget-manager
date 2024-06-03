from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from transaction.tests.factories import TransactionFactory
from .factories import (
    PlaidAccountFactory,
    PlaidItemFactory,
    PlaidTransactionFactory,
)


class TestCascadeDeletes(TestCase):
    def test_transaction_is_deleted_when_plaid_transaction_is_deleted(self):
        """
        Test that a transaction is deleted when its associated PlaidTransaction is deleted
        """
        plaid_transaction = PlaidTransactionFactory()
        transaction = TransactionFactory(plaid_transaction=plaid_transaction)
        plaid_transaction.delete()
        with self.assertRaises(ObjectDoesNotExist):
            transaction.refresh_from_db()

    def test_transaction_is_deleted_when_plaid_account_is_deleted(self):
        """
        Test that a transaction is deleted when its associated PlaidAccount is deleted
        """
        plaid_account = PlaidAccountFactory()
        plaid_transaction = PlaidTransactionFactory(account=plaid_account)
        transaction = TransactionFactory(plaid_transaction=plaid_transaction)
        plaid_account.delete()
        with self.assertRaises(ObjectDoesNotExist):
            transaction.refresh_from_db()

    def test_transaction_is_deleted_when_plaid_item_is_deleted(self):
        """
        Test that a transaction is deleted when its associated PlaidItem is deleted
        """
        plaid_item = PlaidItemFactory()
        plaid_account = PlaidAccountFactory(item=plaid_item)
        plaid_transaction = PlaidTransactionFactory(account=plaid_account)
        transaction = TransactionFactory(plaid_transaction=plaid_transaction)
        plaid_item.delete()
        with self.assertRaises(ObjectDoesNotExist):
            transaction.refresh_from_db()
