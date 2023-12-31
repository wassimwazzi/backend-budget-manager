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
        self.today = datetime.date.today()

    def test_goal_contribution_is_created(self):
        goal = GoalFactory(user=self.user)
        self.assertEqual(GoalContribution.objects.count(), 1)
        goal_contribution = GoalContribution.objects.get()
        self.assertEqual(goal_contribution.goal, goal)

    def test_contribution_percentage_is_set_to_max_possible(self):
        goal = GoalFactory(user=self.user)
        goal_contribution = GoalContribution.objects.get()
        self.assertEqual(goal_contribution.percentage, 100)

    def test_contribution_percentage_is_set_to_max_possible_less_than_100(self):
        prev_goal = GoalFactory(user=self.user)
        prev_contribution = GoalContribution.objects.get()
        prev_contribution.percentage = 50
        prev_contribution.save()
        goal = GoalFactory(
            user=self.user,
            start_date=prev_goal.start_date,
            expected_completion_date=prev_goal.expected_completion_date,
        )
        goal_contribution = GoalContribution.objects.get(goal=goal)
        self.assertEqual(goal_contribution.percentage, 50)

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
        goal2 = GoalFactory(
            user=self.user,
            start_date=goal.start_date,
            expected_completion_date=goal.expected_completion_date,
        )
        self.assertEqual(ContributionRange.objects.count(), 1)

    def test_new_range_is_created_no_overlap(self):
        goal = GoalFactory(user=self.user)
        self.assertEqual(ContributionRange.objects.count(), 1)
        goal2 = GoalFactory(
            user=self.user,
            start_date=goal.expected_completion_date + datetime.timedelta(days=1),
            expected_completion_date=goal.expected_completion_date
            + datetime.timedelta(days=365),
        )
        self.assertEqual(ContributionRange.objects.count(), 2)

    def test_new_range_is_created_overlap(self):
        goal = GoalFactory(
            user=self.user,
            start_date=self.today,
            expected_completion_date=self.today + datetime.timedelta(days=365),
        )
        self.assertEqual(ContributionRange.objects.count(), 1)
        goal2 = GoalFactory(
            user=self.user,
            start_date=goal.start_date + datetime.timedelta(days=40),
            expected_completion_date=goal.expected_completion_date
            + datetime.timedelta(days=365),
        )
        self.assertEqual(ContributionRange.objects.count(), 3)
