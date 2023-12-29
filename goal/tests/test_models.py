from datetime import date
import django.db.utils
from django.test import TestCase
from users.user_factory import UserFactory
from .factories import GoalFactory, GoalContributionFactory
from ..models import GoalContribution


class TestGoalModel(TestCase):
    """
    Test Goal Model
    """

    def setUp(self):
        self.user = UserFactory()
        self.today = date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def test_goal_amount_must_be_positive(self):
        """
        Test goal amount must be positive
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=-1,
                expected_completion_date=self.next_year,
                type="SAVINGS",
                description="Test Goal",
                user=self.user,
            )

    def test_goal_type_must_be_valid(self):
        """
        Test goal type must be valid
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=self.next_year,
                type="INVALID",
                description="Test Goal",
                user=self.user,
            )

    def test_goal_status_must_be_valid(self):
        """
        Test goal status must be valid
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=self.next_year,
                type="SAVINGS",
                description="Test Goal",
                status="INVALID",
                user=self.user,
            )

    def test_goal_start_date_is_set_to_today_if_non_given(self):
        """
        Test goal start date is set to today
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            user=self.user,
        )
        self.assertEqual(goal.start_date, date.today())

    def test_goal_start_date_is_set_to_given_date(self):
        """
        Test goal start date is set to given date
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            start_date=date(2021, 1, 1),
            user=self.user,
        )
        self.assertEqual(goal.start_date, date(2021, 1, 1))

    def test_expected_completion_date_after_start_date(self):
        """
        Test expected completion date after start date
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=date(2020, 1, 1),
                type="SAVINGS",
                description="Test Goal",
                user=self.user,
                start_date=date(2021, 1, 1),
            )

    def test_expected_completion_date_in_future(self):
        """
        Test expected completion date in future
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=date(2020, 1, 1),
                type="SAVINGS",
                description="Test Goal",
                user=self.user,
            )

    def test_expected_completion_date_is_last_day_of_month(self):
        """
        Test expected completion date is last day of month
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year.replace(day=1),
            type="SAVINGS",
            description="Test Goal",
            user=self.user,
        )
        self.assertEqual(goal.expected_completion_date, self.next_year.replace(day=31))

    def test_goal_recurring_frequency_must_be_positive(self):
        """
        Test goal recurring frequency must be positive
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=self.next_year,
                type="SAVINGS",
                description="Test Goal",
                user=self.user,
                recurring=True,
                reccuring_frequency=-1,
            )

    def test_goal_recurring_frequency_defaults_to_none(self):
        """
        Test goal recurring frequency defaults to none
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            user=self.user,
        )
        self.assertIsNone(goal.reccuring_frequency)
        self.assertFalse(goal.recurring)


class TestGoalContributionModel(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.today = date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def test_start_date_is_set_to_first_day_of_month(self):
        """
        Test start date is set to first day of month
        """
        goal_contribution = GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            goal=GoalFactory(),
        )
        self.assertEqual(goal_contribution.start_date, self.today.replace(day=1))

    def test_start_date_defaults_to_first_day_of_month(self):
        """
        Test start date is set to first day of month
        """
        goal_contribution = GoalContributionFactory(
            amount=1000,
            goal=GoalFactory(),
        )
        self.assertEqual(goal_contribution.start_date, self.today.replace(day=1))

    def test_end_date_is_set_to_last_day_of_month(self):
        """
        Test end date is set to last day of month
        """
        goal_contribution = GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            goal=GoalFactory(),
        )
        self.assertEqual(goal_contribution.end_date, self.today.replace(day=31))

    def test_end_date_cannot_be_manually_set(self):
        """
        Test end date cannot be manually set
        """
        goal_contribution = GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            end_date=self.next_year,
            goal=GoalFactory(),
        )
        self.assertEqual(goal_contribution.end_date, self.today.replace(day=31))

    def test_cascade_deletion_of_goal(self):
        """
        Test cascade deletion of goal
        """
        goal = GoalFactory()
        GoalContributionFactory(goal=goal)
        GoalContributionFactory(goal=goal)
        GoalContributionFactory(goal=goal)
        self.assertEqual(goal.goalcontribution_set.count(), 3)
        goal.delete()
        self.assertEqual(GoalContribution.objects.count(), 0)