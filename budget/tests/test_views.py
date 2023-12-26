from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from category.tests.factories import CategoryFactory
from currency.tests.factories import CurrencyFactory
from .factories import BudgetFactory
from ..serializers import BudgetSerializer
from ..models import Budget
import datetime
from decimal import Decimal
from users.user_factory import UserFactory


class TestBudgetView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = CategoryFactory(user=self.user)
        self.currency = CurrencyFactory()
        self.url = "/api/budgets/"

    def test_budget_api_list(self):
        budget = BudgetFactory(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertDictEqual(response.data["results"][0], BudgetSerializer(budget).data)

    def test_budget_list_gets_only_current_user_budgets(self):
        user2 = UserFactory()
        BudgetFactory(user=user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_budget_api_create(self):
        budget_data = {
            "amount": "75.25",
            "currency": self.currency.code,
            "start_date": "2023-02",
            "category": self.category.id,
        }
        response = self.client.post(self.url, budget_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        budget = Budget.objects.get(id=response.data["id"])
        self.assertEqual(budget.amount, Decimal(budget_data["amount"]))
        self.assertEqual(budget.currency.code, budget_data["currency"])
        self.assertEqual(
            budget.start_date,
            datetime.datetime.strptime(budget_data["start_date"], "%Y-%m").date(),
        )
        self.assertEqual(budget.category.id, budget_data["category"])

    def test_budget_api_create_with_invalid_category(self):
        budget_data = {
            "amount": "75.25",
            "currency": self.currency.code,
            "start_date": "2023-02",
            "category": 999,
        }
        response = self.client.post(self.url, budget_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_budget_api_create_with_invalid_currency(self):
        budget_data = {
            "amount": "75.25",
            "currency": "XXX",
            "start_date": "2023-02",
            "category": self.category.id,
        }
        response = self.client.post(self.url, budget_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_budget_api_create_with_invalid_start_date(self):
        budget_data = {
            "amount": "75.25",
            "currency": self.currency.code,
            "start_date": "20232-02-01",
            "category": self.category.id,
        }
        response = self.client.post(self.url, budget_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_budget_api_retrieve(self):
        budget = BudgetFactory(user=self.user)
        response = self.client.get(self.url + f"{budget.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, BudgetSerializer(budget).data)

    def test_budget_api_update(self):
        budget = BudgetFactory(user=self.user)
        updated_data = {
            "amount": "50.75",
            "currency": self.currency.code,
            "start_date": "2023-03",
            "category": self.category.id,
        }
        response = self.client.put(
            self.url + f"{budget.id}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertEqual(response.data["amount"], updated_data["amount"])
        self.assertEqual(response.data["currency"], updated_data["currency"])
        self.assertEqual(
            response.data["start_date"],
            updated_data["start_date"],
        )
        self.assertEqual(response.data["category"]["id"], updated_data["category"])

    def test_partial_budget_update(self):
        budget = BudgetFactory(user=self.user)
        old_data = BudgetSerializer(budget).data
        updated_data = {"amount": "50.75"}
        response = self.client.patch(
            self.url + f"{budget.id}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertNotEqual(response.data["amount"], old_data["amount"])
        self.assertEqual(response.data["amount"], updated_data["amount"])

    def test_partial_update_category_does_not_exist(self):
        budget = BudgetFactory(user=self.user)
        old_data = BudgetSerializer(budget).data
        updated_data = {"category": 999}
        response = self.client.patch(
            self.url + f"{budget.id}/", data=updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Budget.objects.count(), 1)
        self.assertDictEqual(BudgetSerializer(budget).data, old_data)

    def test_budget_api_delete(self):
        budget = BudgetFactory(user=self.user)
        response = self.client.delete(self.url + f"{budget.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Budget.objects.count(), 0)

    def test_budget_api_summary(self):
        start_date = datetime.date(2023, 2, 1)
        self.category.income = False
        self.category.save()
        budget = BudgetFactory(user=self.user, start_date=start_date, category=self.category)
        response = self.client.get(self.url + "summary/", {"month": "2023-02"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["category"], budget.category.category)
        self.assertEqual(response.data[0]["budget"], budget.amount)
        self.assertEqual(response.data[0]["actual"], 0)
        self.assertEqual(response.data[0]["remaining"], budget.amount)

    def test_budget_api_summary_invalid_month(self):
        response = self.client.get(self.url + "summary/", {"month": "2023-13"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "month must be in YYYY-MM format")

    def test_budget_api_summary_invalid_month_format(self):
        response = self.client.get(self.url + "summary/", {"month": "2023-12-01"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "month must be in YYYY-MM format")

    def test_budget_api_summary_no_month(self):
        response = self.client.get(self.url + "summary/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "month param is required")