import datetime
import django.db.utils
from django.test import TestCase
from users.user_factory import UserFactory
from .factories import GoalFactory, GoalContributionFactory
from ..models import GoalContribution
from transaction.tests.factories import TransactionFactory
from transaction.tests.factories import CategoryFactory


class TestGoalModel(TestCase):
    """
    Test Goal Model
    """

    def setUp(self):
        self.user = UserFactory()
        self.today = datetime.date.today()
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

    def test_goal_start_date_default_if_non_given(self):
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
        self.assertEqual(goal.start_date, datetime.date.today().replace(day=1))

    def test_goal_start_date_is_set_to_first_day_of_month(self):
        """
        Test goal start date is set to given date
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            start_date=datetime.date(2021, 1, 15),
            user=self.user,
        )
        self.assertEqual(goal.start_date, datetime.date(2021, 1, 1))

    def test_expected_completion_date_after_start_date(self):
        """
        Test expected completion date after start date
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=datetime.date(2020, 1, 1),
                type="SAVINGS",
                description="Test Goal",
                user=self.user,
                start_date=datetime.date(2021, 1, 1),
            )

    def test_expected_completion_date_in_future(self):
        """
        Test expected completion date in future
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=datetime.date(2020, 1, 1),
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
        self.assertEqual(goal.recurring, "NON_RECURRING")

    def test_actual_completion_date_is_set_to_today_when_status_is_completed(self):
        """
        Test actual completion date is set to today when status is completed
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            user=self.user,
            status="COMPLETED",
        )
        self.assertEqual(goal.actual_completion_date, datetime.date.today())

    def test_actual_completion_date_is_set_to_none_when_status_is_not_completed(self):
        """
        Test actual completion date is set to none when status is not completed
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            user=self.user,
            status="PENDING",
        )
        self.assertIsNone(goal.actual_completion_date)

    def test_cannot_set_actual_completion_date_if_status_is_not_completed(self):
        """
        Test cannot set actual completion date if status is not completed
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=self.next_year,
                type="SAVINGS",
                description="Test Goal",
                user=self.user,
                status="PENDING",
                actual_completion_date=datetime.date.today(),
            )

    def test_manually_setting_actual_completion_date(self):
        """
        Test manually setting actual completion date
        """
        actual_completion_date = self.next_year - datetime.timedelta(days=30)
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            user=self.user,
            status="COMPLETED",
            actual_completion_date=actual_completion_date,
        )
        self.assertEqual(goal.actual_completion_date, actual_completion_date)

    def test_actual_completion_date_must_be_after_start_date(self):
        """
        Test actual completion date must be after start date
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalFactory(
                amount=1000,
                expected_completion_date=self.next_year,
                type="SAVINGS",
                description="Test Goal",
                user=self.user,
                status="COMPLETED",
                actual_completion_date=datetime.date(2020, 1, 1),
            )

    def test_actual_completion_date_can_be_after_expected_completion_date(self):
        """
        Test actual completion date can be after expected completion date
        """
        actual_completion_date = self.next_year + datetime.timedelta(days=30)
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            type="SAVINGS",
            description="Test Goal",
            user=self.user,
            status="COMPLETED",
            actual_completion_date=actual_completion_date,
        )
        self.assertEqual(goal.actual_completion_date, actual_completion_date)


class TestGoalContributionModel(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def test_start_date_is_set_to_first_day_of_month(self):
        """
        Test start date is set to first day of month
        """
        goal_contribution = GoalContributionFactory(
            amount=1000,
            start_date=self.today,
        )
        self.assertEqual(goal_contribution.start_date, self.today.replace(day=1))

    def test_start_date_defaults_to_first_day_of_month(self):
        """
        Test start date is set to first day of month
        """
        goal_contribution = GoalContributionFactory(
            amount=1000,
        )
        self.assertEqual(goal_contribution.start_date, self.today.replace(day=1))

    def test_end_date_is_set_to_last_day_of_month(self):
        """
        Test end date is set to last day of month
        """
        goal_contribution = GoalContributionFactory(
            amount=1000,
            start_date=self.today,
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

    def test_percentage_must_be_between_0_and_100(self):
        """
        Test percentage must be between 0 and 100
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                start_date=self.today,
                percentage=101,
            )

    def test_percentage_must_be_positive(self):
        """
        Test percentage must be positive
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                start_date=self.today,
                percentage=-1,
            )

    def test_cannot_have_two_overlapping_contributions_to_the_same_goal(self):
        """
        Test cannot have two overlapping contributions to the same goal
        """
        goal = GoalFactory()
        GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            goal=goal,
            percentage=10,  # so percentage validation doesn't fail
        )
        with self.assertRaises(django.db.utils.IntegrityError):
            GoalContributionFactory(
                amount=1000,
                start_date=self.today,
                goal=goal,
                percentage=10,
            )

    def test_percentages_over_a_month_cannot_sum_to_more_than_100(self):
        """
        Test percentages cannot sum to more than 100
        """
        goal1 = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        goal2 = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            goal=goal1,
            percentage=50,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                start_date=self.today,
                goal=goal2,
                percentage=51,
            )

    def test_percentages_over_a_month_can_over_100_for_different_users(self):
        """
        Test percentages can sum to more than 100 for different users
        """
        user2 = UserFactory()
        goal1 = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        goal2 = GoalFactory(
            start_date=self.today, expected_completion_date=self.next_year, user=user2
        )
        GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            goal=goal1,
            percentage=50,
        )
        GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            goal=goal2,
            percentage=51,
        )

    def test_percentages_can_sum_over_100_if_they_dont_overlap(self):
        """
        Test percentages can sum to more than 100 if they don't overlap
        """
        goal1 = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        goal2 = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        GoalContributionFactory(
            amount=1000,
            start_date=self.today,
            goal=goal1,
            percentage=50,
        )
        GoalContributionFactory(
            amount=1000,
            start_date=self.today + datetime.timedelta(days=60),
            goal=goal2,
            percentage=51,
        )

    def test_cannot_create_contribution_for_completed_goal(self):
        """
        Test cannot create contribution for completed goal
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
            status="COMPLETED",
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                start_date=self.today,
                goal=goal,
            )


class TestCalculateContributionAmount(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def test_happy_path(self):
        """
        Test happy path
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            start_date=self.today,
            goal=goal,
            percentage=100,
        )
        income = TransactionFactory(
            user=self.user,
            amount=1000,
            date=self.today,
            category=CategoryFactory(income=True, user=self.user),
        )
        expense = TransactionFactory(
            user=self.user,
            amount=300,
            date=self.today,
            category=CategoryFactory(income=False, user=self.user),
        )
        self.assertEqual(contribution.contribution, 700)

    def test_applies_percentage(self):
        """
        Test applies percentage
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            start_date=self.today,
            goal=goal,
            percentage=50,
        )
        income = TransactionFactory(
            user=self.user,
            amount=1000,
            date=self.today,
            category=CategoryFactory(income=True, user=self.user),
        )
        expense = TransactionFactory(
            user=self.user,
            amount=300,
            date=self.today,
            category=CategoryFactory(income=False, user=self.user),
        )
        self.assertEqual(contribution.contribution, 350)

    def test_sums_transactions(self):
        """
        Test sums transactions
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            start_date=self.today,
            goal=goal,
            percentage=100,
        )
        income = TransactionFactory(
            user=self.user,
            amount=1000,
            date=self.today,
            category=CategoryFactory(income=True, user=self.user),
        )
        income2 = TransactionFactory(
            user=self.user,
            amount=1000,
            date=self.today,
            category=CategoryFactory(income=True, user=self.user),
        )
        expense = TransactionFactory(
            user=self.user,
            amount=300,
            date=self.today,
            category=CategoryFactory(income=False, user=self.user),
        )
        expense2 = TransactionFactory(
            user=self.user,
            amount=300,
            date=self.today,
            category=CategoryFactory(income=False, user=self.user),
        )
        self.assertEqual(contribution.contribution, 1400)

    def test_does_not_sum_transactions_outside_of_date_range(self):
        """
        Test does not sum transactions outside of date range
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            start_date=self.today,
            goal=goal,
            percentage=100,
        )
        income = TransactionFactory(
            user=self.user,
            amount=1000,
            date=self.today,
            category=CategoryFactory(income=True, user=self.user),
        )
        outside_range = TransactionFactory(
            user=self.user,
            amount=1000,
            date=contribution.start_date - datetime.timedelta(days=1),
            category=CategoryFactory(income=True, user=self.user),
        )
        expense = TransactionFactory(
            user=self.user,
            amount=300,
            date=self.today,
            category=CategoryFactory(income=False, user=self.user),
        )
        self.assertEqual(contribution.contribution, 700)

    def test_does_not_sum_transactions_for_other_users(self):
        """
        Test does not sum transactions for other users
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            start_date=self.today,
            goal=goal,
            percentage=100,
        )
        other_user = UserFactory()
        other_user_transaction = TransactionFactory(
            user=other_user,
            date=self.today,
        )
        self.assertEqual(contribution.contribution, 0)

    def test_uses_amount_if_it_exists(self):
        """
        Test uses amount if it exists
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            start_date=self.today,
            goal=goal,
            percentage=100,
            amount=1000,
        )
        income = TransactionFactory(
            user=self.user,
            amount=1000,
            date=self.today,
            category=CategoryFactory(income=True, user=self.user),
        )
        expense = TransactionFactory(
            user=self.user,
            amount=300,
            date=self.today,
            category=CategoryFactory(income=False, user=self.user),
        )
        self.assertEqual(contribution.contribution, 1000)
