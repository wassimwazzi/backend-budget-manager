from django.test import TestCase
from users.user_factory import UserFactory
from rest_framework.test import APIClient
from rest_framework import status
from category.tests.factories import CategoryFactory
from currency.tests.factories import CurrencyFactory
from .factories import TransactionFactory
from ..serializers import TransactionSerializer
from ..models import Transaction
from datetime import date


class TransactionAPITestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
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
        self.assertDictEqual(
            response.data["results"][0], TransactionSerializer(transaction).data
        )

    def test_transaction_list_filter_by_code(self):
        transaction1 = TransactionFactory(user=self.user, code="123")
        transaction2 = TransactionFactory(user=self.user, code="456")
        response = self.client.get(
            self.url, {"filter[]": "code", "filter_value[]": transaction2.code}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertDictEqual(
            response.data["results"][0], TransactionSerializer(transaction2).data
        )

    def test_transaction_list_filter_by_category(self):
        transaction1 = TransactionFactory(user=self.user, category=self.category)
        transaction2 = TransactionFactory(user=self.user)
        response = self.client.get(
            self.url,
            {"filter[]": "category", "filter_value[]": transaction1.category.category},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertDictEqual(
            response.data["results"][0], TransactionSerializer(transaction1).data
        )

    def test_transaction_list_does_not_return_other_users_transactions(self):
        user2 = UserFactory(username="testuser2", password="testpassword2")
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

    def test_transaction_api_create_auto_uses_current_user(self):
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
        transaction = Transaction.objects.get(id=response.data["id"])
        self.assertEqual(transaction.user, self.user)

    def test_transaction_api_create_cannot_set_other_user(self):
        user2 = UserFactory(username="testuser2", password="testpassword2")
        transaction_data = {
            "code": "456",
            "amount": "75.25",
            "currency": self.currency.code,
            "date": "2023-02-01",
            "description": "API test transaction",
            "category": self.category.id,
            "user": user2.id,
        }
        response = self.client.post(self.url, data=transaction_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(id=response.data["id"])
        self.assertEqual(transaction.user, self.user)

    def test_transaction_api_create_cannot_set_other_users_category(self):
        user2 = UserFactory(username="testuser2", password="testpassword2")
        category2 = CategoryFactory(user=user2)
        transaction_data = {
            "code": "456",
            "amount": "75.25",
            "currency": self.currency.code,
            "date": "2023-02-01",
            "description": "API test transaction",
            "category": category2.id,
        }
        response = self.client.post(self.url, data=transaction_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        user2 = UserFactory(username="testuser2", password="testpassword2")
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
        user2 = UserFactory(username="testuser2", password="testpassword2")
        transaction = TransactionFactory(user=user2)
        response = self.client.delete(self.url + f"{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Transaction.objects.count(), 1)


class TestSpendByCategory(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/transactions/spend_by_category/"
        self.transactions = TransactionFactory.create_batch(
            3, user=self.user, category__income=False
        )

    def test_spend_by_category(self):
        # Also validates that they are sorted by total descending
        self.transactions[0].amount = 300
        self.transactions[1].amount = 200
        self.transactions[2].amount = 100
        self.transactions[0].save()
        self.transactions[1].save()
        self.transactions[2].save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            response.data[0]["category"], self.transactions[0].category.category
        )
        self.assertEqual(response.data[0]["total"], self.transactions[0].amount)
        self.assertEqual(
            response.data[1]["category"], self.transactions[1].category.category
        )
        self.assertEqual(response.data[1]["total"], self.transactions[1].amount)
        self.assertEqual(
            response.data[2]["category"], self.transactions[2].category.category
        )
        self.assertEqual(response.data[2]["total"], self.transactions[2].amount)

    def test_spend_by_category_monthly(self):
        response = self.client.get(self.url, {"monthly": True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            response.data[0]["category"], self.transactions[0].category.category
        )
        self.assertEqual(
            response.data[0]["month"], self.transactions[0].date.strftime("%Y-%m")
        )
        self.assertEqual(response.data[0]["total"], self.transactions[0].amount)
        self.assertEqual(
            response.data[1]["category"], self.transactions[1].category.category
        )
        self.assertEqual(
            response.data[1]["month"], self.transactions[1].date.strftime("%Y-%m")
        )
        self.assertEqual(response.data[1]["total"], self.transactions[1].amount)
        self.assertEqual(
            response.data[2]["category"], self.transactions[2].category.category
        )
        self.assertEqual(
            response.data[2]["month"], self.transactions[2].date.strftime("%Y-%m")
        )
        self.assertEqual(response.data[2]["total"], self.transactions[2].amount)

    def test_spend_by_category_monthly_filter_by_category(self):
        response = self.client.get(
            self.url,
            {
                "monthly": True,
                "filter[]": "category",
                "filter_value[]": self.transactions[0].category.category,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["category"], self.transactions[0].category.category
        )
        self.assertEqual(
            response.data[0]["month"], self.transactions[0].date.strftime("%Y-%m")
        )
        self.assertEqual(response.data[0]["total"], self.transactions[0].amount)

    def test_spend_by_category_monthly_filter_by_category_does_not_exist(self):
        response = self.client.get(
            self.url,
            {
                "monthly": True,
                "filter[]": "category",
                "filter_value[]": "does not exist",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_spend_by_category_sums_up_transactions(self):
        Transaction.objects.all().delete()
        transaction1 = TransactionFactory(
            user=self.user, category__income=False, amount=100
        )
        TransactionFactory(user=self.user, category=transaction1.category, amount=200)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["category"], transaction1.category.category)
        self.assertEqual(response.data[0]["total"], 300)

    def test_spend_by_category_does_not_include_income(self):
        Transaction.objects.all().delete()
        TransactionFactory(user=self.user, category__income=True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class TestSpendVsIncomeByMonth(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/transactions/spend_vs_income_by_month/"

    def test_spend_vs_income_by_month(self):
        TransactionFactory(user=self.user, category__income=False, amount=100)
        TransactionFactory(user=self.user, category__income=True, amount=1000)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["month"],
            Transaction.objects.first().date.strftime("%Y-%m"),
        )
        self.assertEqual(response.data[0]["spend"], 100)
        self.assertEqual(response.data[0]["income"], 1000)

    def test_spend_vs_income_by_month_multiple_months(self):
        month1 = date(2021, 1, 1)
        month2 = date(2021, 2, 1)
        TransactionFactory(
            user=self.user, category__income=False, amount=100, date=month1
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=1000, date=month1
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=200, date=month2
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=2000, date=month2
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["month"], month2.strftime("%Y-%m"))
        self.assertEqual(response.data[0]["spend"], 200)
        self.assertEqual(response.data[0]["income"], 2000)
        self.assertEqual(response.data[1]["month"], month1.strftime("%Y-%m"))
        self.assertEqual(response.data[1]["spend"], 100)
        self.assertEqual(response.data[1]["income"], 1000)


class TestSummarize(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/transactions/summary/"

    def test_average_spend_by_month(self):
        TransactionFactory(
            user=self.user, category__income=False, amount=100, date=date(2021, 1, 1)
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=200, date=date(2021, 1, 10)
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=300, date=date(2021, 1, 15)
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=100, date=date(2021, 2, 1)
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=200, date=date(2021, 2, 9)
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=300, date=date(2021, 2, 16)
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=300, date=date(2021, 2, 26)
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["monthly_average"]["spend"],
            300,
        )
        self.assertEqual(
            response.data["monthly_average"]["income"],
            450,
        )

    def test_average_spend_by_month_no_transactions(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["monthly_average"]["spend"],
            0,
        )
        self.assertEqual(
            response.data["monthly_average"]["income"],
            0,
        )

    def test_average_spend_by_month_only_income(self):
        TransactionFactory(
            user=self.user, category__income=True, amount=300, date=date(2021, 1, 15)
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=300, date=date(2021, 2, 16)
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=300, date=date(2021, 2, 26)
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["monthly_average"]["spend"],
            0,
        )
        self.assertEqual(
            response.data["monthly_average"]["income"],
            450,
        )

    def test_average_spend_by_month_only_spend(self):
        TransactionFactory(
            user=self.user, category__income=False, amount=100, date=date(2021, 1, 1)
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=200, date=date(2021, 1, 10)
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=100, date=date(2021, 2, 1)
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=200, date=date(2021, 2, 9)
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["monthly_average"]["spend"],
            300,
        )
        self.assertEqual(
            response.data["monthly_average"]["income"],
            0,
        )

    def test_average_spend_by_month_only_one_month(self):
        TransactionFactory(
            user=self.user, category__income=False, amount=100, date=date(2021, 1, 1)
        )
        TransactionFactory(
            user=self.user, category__income=False, amount=200, date=date(2021, 1, 10)
        )
        TransactionFactory(
            user=self.user, category__income=True, amount=300, date=date(2021, 1, 15)
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["monthly_average"]["spend"],
            300,
        )
        self.assertEqual(
            response.data["monthly_average"]["income"],
            300,
        )
