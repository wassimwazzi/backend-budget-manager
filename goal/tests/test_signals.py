import datetime
import django.db.utils
from django.test import TestCase
from users.user_factory import UserFactory
from .factories import GoalFactory, GoalContributionFactory, ContributionRangeFactory
from ..models import GoalContribution, ContributionRange, Goal
from transaction.tests.factories import TransactionFactory
from transaction.tests.factories import CategoryFactory


class TestOnGoalCreateSignal(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_goal_contribution_is_created(self):
        goal = GoalFactory(user=self.user)
        self.assertEqual(GoalContribution.objects.count(), 1)
        goal_contribution = GoalContribution.objects.get()
        self.assertEqual(goal_contribution.goal, goal)

    def test_contribution_percentage_is_set_to_max_possible(self):
        goal = GoalFactory(user=self.user)
        goal_contribution = GoalContribution.objects.get()
        self.assertEqual(goal_contribution.percentage, 100)

    def test_contribution_range_is_created(self):
        goal = GoalFactory(user=self.user)
        self.assertEqual(ContributionRange.objects.count(), 1)
        contribution_range = ContributionRange.objects.get()
        self.assertEqual(contribution_range.start_date, goal.start_date)
        self.assertEqual(contribution_range.end_date, goal.expected_completion_date)

    def test_contribution_is_assigned_to_range(self):
        goal = GoalFactory(user=self.user)
        goal_contribution = GoalContribution.objects.get()
        contribution_range = ContributionRange.objects.get()
        self.assertEqual(goal_contribution.date_range, contribution_range)

    def test_contribution_range_is_not_created_if_already_exists(self):
        goal = GoalFactory(user=self.user)
        self.assertEqual(ContributionRange.objects.count(), 1)
        goal2 = GoalFactory(user=self.user)
        self.assertEqual(ContributionRange.objects.count(), 1)
