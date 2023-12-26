from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from category.tests.factories import CategoryFactory
from currency.tests.factories import CurrencyFactory
from ..serializers import CategorySerializer
from ..models import Category
from users.user_factory import UserFactory


class TestCategoryView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        Category.objects.all().delete()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.category = CategoryFactory(user=self.user)
        self.currency = CurrencyFactory()
        self.url = "/api/categories/"

    def test_category_api_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertDictEqual(response.data["results"][0], CategorySerializer(self.category).data)

    def test_category_list_gets_only_current_user_categories(self):
        user2 = UserFactory()
        CategoryFactory(user=user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1) # self.category

    def test_list_pagination_off(self):
        response = self.client.get(self.url, {"paginate": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0], CategorySerializer(self.category).data)

    def test_list_pagination_on(self):
        response = self.client.get(self.url, {"paginate": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0], CategorySerializer(self.category).data)

    def test_category_api_create(self):
        category_data = {
            "category": "Test Category",
            "description": "Test Description",
            "income": False,
        }
        response = self.client.post(self.url, category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category = Category.objects.get(id=response.data["id"])
        self.assertEqual(category.category, category_data["category"])
        self.assertEqual(category.description, category_data["description"])
        self.assertEqual(category.income, category_data["income"])