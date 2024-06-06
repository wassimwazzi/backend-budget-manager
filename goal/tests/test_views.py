from django.test import TestCase
from users.user_factory import UserFactory
from goal.tests.factories import GoalFactory, GoalContributionFactory
from goal.models import Goal, GoalContribution
from rest_framework.test import APIClient
from rest_framework import status
from goal.serializers import GoalSerializer
import datetime
from decimal import Decimal


class TestGoalView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/goals/"
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def test_goal_api_list(self):
        goal = GoalFactory(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data[0], GoalSerializer(goal).data)

    def test_goal_list_gets_only_current_user_goals(self):
        user2 = UserFactory()
        GoalFactory(user=user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_goal_api_create(self):
        goal_data = {
            "amount": "75",
            "expected_completion_date": self.next_year.strftime("%Y-%m"),
            "type": "SAVINGS",
            "description": "test goal",
            "status": "IN_PROGRESS",
            "start_date": "2020-02",
            "recurring": "NON_RECURRING",
        }
        response = self.client.post(self.url, goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        goal = Goal.objects.get(id=response.data["id"])
        self.assertEqual(goal.amount, Decimal(goal_data["amount"]))
        self.assertEqual(goal.type, goal_data["type"])
        self.assertEqual(goal.description, goal_data["description"])
        self.assertEqual(goal.status, goal_data["status"])
        self.assertEqual(goal.recurring, goal_data["recurring"])

    def test_goal_api_create_with_invalid_data(self):
        goal_data = {
            "amount": "75",
            "expected_completion_date": "2020-02",
            "type": "SAVINGS",
            "description": "test goal",
            "status": "IN_PROGRESS",
            "start_date": "2020-02",
            "recurring": "NON_RECURRING",
            "user": self.user.id,
        }
        response = self.client.post(self.url, goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_goal_api_create_with_invalid_recurring(self):
        goal_data = {
            "amount": "75",
            "expected_completion_date": self.next_year.strftime("%Y-%m"),
            "type": "SAVINGS",
            "description": "test goal",
            "status": "IN_PROGRESS",
            "start_date": "2020-02",
            "recurring": "FIXED",
            # missing recurring_frequency
            "user": self.user.id,
        }
        response = self.client.post(self.url, goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_goal_api_patch(self):
        goal = GoalFactory(user=self.user)
        goal_data = {
            "amount": "75",
            "expected_completion_date": self.next_year.strftime("%Y-%m"),
            "type": "SAVINGS",
            "description": "test goal",
            "status": "IN_PROGRESS",
            "start_date": "2020-02",
            "recurring": "NON_RECURRING",
            "user": self.user.id,
        }
        response = self.client.patch(f"{self.url}{goal.id}/", goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.amount, Decimal(goal_data["amount"]))
        self.assertEqual(goal.type, goal_data["type"])
        self.assertEqual(goal.description, goal_data["description"])
        self.assertEqual(goal.status, goal_data["status"])
        self.assertEqual(goal.recurring, goal_data["recurring"])

    def test_goal_api_update(self):
        goal = GoalFactory(user=self.user)
        goal_data = {
            "amount": "75",
            "expected_completion_date": self.next_year.strftime("%Y-%m"),
            "type": "SAVINGS",
            "description": "test goal",
            "status": "IN_PROGRESS",
            "start_date": "2020-02",
            "recurring": "NON_RECURRING",
            "user": self.user.id,
        }
        response = self.client.put(f"{self.url}{goal.id}/", goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal.refresh_from_db()
        self.assertEqual(goal.amount, Decimal(goal_data["amount"]))
        self.assertEqual(goal.type, goal_data["type"])
        self.assertEqual(goal.description, goal_data["description"])
        self.assertEqual(goal.status, goal_data["status"])
        self.assertEqual(goal.recurring, goal_data["recurring"])
