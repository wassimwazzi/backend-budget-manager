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
        self.assertEqual(response.data["count"], 1)
        self.assertDictEqual(response.data["results"][0], GoalSerializer(goal).data)

    def test_goal_list_gets_only_current_user_goals(self):
        user2 = UserFactory()
        GoalFactory(user=user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_goal_api_create(self):
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
            "user": self.user.id,
        }
        response = self.client.post(self.url, goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_goal_api_create_with_goal_contributions(self):
        goal_data = {
            "amount": "10000",
            "expected_completion_date": "2024-12",
            "type": "SAVINGS",
            "start_date": "2024-01-01",
            "description": "API test goal",
            "contributions": [
                {"start_date": "2024-01-01", "percentage": 100},
                {"start_date": "2024-03-01", "percentage": 50},
            ],
        }
        response = self.client.post(self.url, goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        goal = Goal.objects.get(id=response.data["id"])
        self.assertEqual(goal.amount, Decimal(goal_data["amount"]))
        self.assertEqual(
            goal.expected_completion_date,
            datetime.datetime.strptime("2024-12-31", "%Y-%m-%d").date(),
        )
        self.assertEqual(goal.type, goal_data["type"])
        self.assertEqual(goal.description, goal_data["description"])
        self.assertEqual(goal.status, "IN_PROGRESS")
        self.assertEqual(
            goal.start_date,
            datetime.datetime.strptime(goal_data["start_date"], "%Y-%m-%d").date(),
        )
        self.assertEqual(goal.recurring, "NON_RECURRING")
        self.assertEqual(goal.contributions.count(), 2)
        contributions = goal.contributions.order_by("start_date")
        self.assertEqual(
            contributions.first().start_date,
            datetime.datetime.strptime(
                goal_data["contributions"][0]["start_date"], "%Y-%m-%d"
            ).date(),
        )
        self.assertEqual(
            contributions.first().percentage,
            goal_data["contributions"][0]["percentage"],
        )
        self.assertEqual(
            contributions.last().start_date,
            datetime.datetime.strptime(
                goal_data["contributions"][1]["start_date"], "%Y-%m-%d"
            ).date(),
        )

    def test_goal_api_create_with_invalid_goal_contributions(self):
        goal_data = {
            "amount": "10000",
            "expected_completion_date": "2024-12",
            "type": "SAVINGS",
            "start_date": "2024-01-01",
            "description": "API test goal",
            "contributions": [
                {"start_date": "2024-01-01", "percentage": 100},
                {"start_date": "2024-03-01", "percentage": 101},
            ],
        }
        response = self.client.post(self.url, goal_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["contributions"][1]["percentage"][0],
            "Ensure this value is less than or equal to 100.",
        )
        self.assertFalse(Goal.objects.exists())
        self.assertFalse(GoalContribution.objects.exists())

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

    def test_goal_api_update_raises_405(self):
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
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
