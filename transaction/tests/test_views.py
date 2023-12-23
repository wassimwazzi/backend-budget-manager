from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from category.tests.factories import CategoryFactory
from currency.tests.factories import CurrencyFactory
from .factories import TransactionFactory
from ..serializers import TransactionSerializer
from ..models import Transaction


class TransactionAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = CategoryFactory(user=self.user)
        self.currency = CurrencyFactory()
        self.url = "/api/transactions/"

    def test_transaction_api_list(self):
        transaction = TransactionFactory(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertDictEqual(response.data["results"][0], TransactionSerializer(transaction).data)

    def test_transaction_list_filter_by_code(self):
        transaction1 = TransactionFactory(user=self.user)
        transaction2 = TransactionFactory(user=self.user)
        response = self.client.get(self.url, {"filter": "code", "filter_value": transaction2.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertDictEqual(response.data["results"][0], TransactionSerializer(transaction2).data)

    def test_transaction_list_does_not_return_other_users_transactions(self):
        user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        TransactionFactory(user=user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_transaction_api_create(self):
        transaction_data = {
            "code": "456",
            "amount": "75.25",
            "currency": self.currency.code,
            "date": "2023-02-01",
            "description": "API test transaction",
            "category": self.category.id,
        }
        response = self.client.post(self.url, data=transaction_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_transaction_api_retrieve(self):
        transaction = TransactionFactory(user=self.user)
        response = self.client.get(self.url + f"{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, TransactionSerializer(transaction).data)

    def test_transaction_api_update(self):
        transaction = TransactionFactory(user=self.user)
        updated_data = {
            "code": "789",
            "amount": "50.75",
            "currency": self.currency.code,
            "date": "2023-03-01",
            "description": "API test transaction updated",
            "category": self.category.id,
        }
        response = self.client.put(
            self.url + f"{transaction.id}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(response.data["description"], updated_data["description"])
        self.assertEqual(response.data["code"], updated_data["code"])
        self.assertEqual(response.data["amount"], updated_data["amount"])
        self.assertEqual(response.data["currency"], updated_data["currency"])
        self.assertEqual(response.data["date"], updated_data["date"])
        self.assertEqual(response.data["category"]["id"], updated_data["category"])

    def test_partial_transaction_update(self):
        transaction = TransactionFactory(user=self.user)
        old_data = TransactionSerializer(transaction).data
        updated_data = {"description": "API test transaction updated"}
        response = self.client.patch(
            self.url + f"{transaction.id}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertNotEqual(response.data["description"], old_data["description"])
        self.assertEqual(response.data["description"], updated_data["description"])

    def test_partial_update_category_does_not_exist(self):
        transaction = TransactionFactory(user=self.user)
        old_data = TransactionSerializer(transaction).data
        updated_data = {"category": 999}
        response = self.client.patch(
            self.url + f"{transaction.id}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertDictEqual(TransactionSerializer(transaction).data, old_data)

    def test_transaction_cannot_update_other_users_transactions(self):
        user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        transaction = TransactionFactory(user=user2)
        old_data = TransactionSerializer(transaction).data
        updated_data = {
            "code": "789",
            "amount": "50.75",
            "currency": self.currency.code,
            "date": "2023-03-01",
            "description": "API test transaction updated",
            "category": self.category.category,
        }
        response = self.client.put(
            self.url + f"{transaction.id}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertDictEqual(TransactionSerializer(transaction).data, old_data)

    def test_transaction_api_delete(self):
        transaction = TransactionFactory(user=self.user)
        response = self.client.delete(self.url + f"{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_cannot_delete_other_users_transactions(self):
        user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        transaction = TransactionFactory(user=user2)
        response = self.client.delete(self.url + f"{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Transaction.objects.count(), 1)
