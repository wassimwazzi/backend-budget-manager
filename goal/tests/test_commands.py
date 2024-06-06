from django.test import TestCase
from ..models import GoalStatus
from .factories import GoalFactory, Goal, GoalRecurranceType
from transaction.tests.factories import TransactionFactory
from category.tests.factories import CategoryFactory
from django.core.management import call_command
from io import StringIO
import datetime
from unittest.mock import patch
from freezegun import freeze_time


class TestUpdateStatus(TestCase):
    def test_sets_status_to_failed(self):
        goal = GoalFactory(
            status=GoalStatus.IN_PROGRESS,
            expected_completion_date=datetime.date.today(),
        )
        with freeze_time(goal.expected_completion_date + datetime.timedelta(days=10)):
            call_command("update_status", stdout=StringIO())
        goal.refresh_from_db()
        self.assertEqual(goal.status, GoalStatus.FAILED)

    def test_sets_status_to_completed(self):
        goal = GoalFactory(
            status=GoalStatus.IN_PROGRESS,
            expected_completion_date=datetime.date.today(),
        )
        income_category = CategoryFactory(income=True, user=goal.user)
        TransactionFactory(
            amount=goal.amount,
            date=goal.start_date,
            user=goal.user,
            category=income_category,
        )
        with freeze_time(goal.expected_completion_date + datetime.timedelta(days=10)):
            call_command("update_status", stdout=StringIO())
        goal.refresh_from_db()
        self.assertEqual(goal.status, GoalStatus.COMPLETED)

    def test_sets_status_to_in_progress(self):
        goal = GoalFactory(status=GoalStatus.PENDING, start_date=datetime.date.today())
        call_command("update_status", stdout=StringIO())
        goal.refresh_from_db()
        self.assertEqual(goal.status, GoalStatus.IN_PROGRESS)


class TestCreateGoals(TestCase):
    def test_creates_goals(self):
        goal = GoalFactory(
            recurring=GoalRecurranceType.FIXED,
            recurring_frequency=1,
            expected_completion_date=datetime.date.today(),
            start_date=datetime.date.today() - datetime.timedelta(weeks=5),
        )
        with freeze_time(goal.expected_completion_date + datetime.timedelta(weeks=5)):
            call_command("create_goals", stdout=StringIO())
        self.assertEqual(Goal.objects.count(), 2)
        self.assertEqual(Goal.objects.filter(previous_goal=goal).count(), 1)
        self.assertEqual(Goal.objects.filter(previous_goal__isnull=True).count(), 1)
