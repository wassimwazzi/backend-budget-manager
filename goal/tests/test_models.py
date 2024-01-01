import datetime
import django.db.utils
from django.db.models.signals import post_save
from django.test import TestCase
from users.user_factory import UserFactory
from .factories import GoalFactory, GoalContributionFactory, ContributionRangeFactory
from ..models import GoalContribution, Goal, ContributionRange
from ..signals import on_goal_create
from ..serializers import GoalSmallSerializer
from transaction.tests.factories import TransactionFactory
from transaction.tests.factories import CategoryFactory


class TestGoalModel(TestCase):
    """
    Test Goal Model
    """

    def setUp(self):
        post_save.disconnect(sender=Goal, receiver=on_goal_create)
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def tearDown(self):
        post_save.connect(sender=Goal, receiver=on_goal_create)

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


class TestGoalProgress(TestCase):
    def setUp(self):
        post_save.disconnect(sender=Goal, receiver=on_goal_create)
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)
        self.goal = GoalFactory(
            amount=1000, expected_completion_date=self.next_year, user=self.user
        )
        self.goal_midpoint = (
            self.goal.start_date
            + (self.goal.expected_completion_date - self.goal.start_date) / 2
        )

    def tearDown(self):
        post_save.connect(sender=Goal, receiver=on_goal_create)

    def test_progress_is_0_if_no_contributions(self):
        """
        Test progress is 0 if no contributions
        """
        self.assertEqual(self.goal.total_contributed, 0)

    def test_sums_up_contributions(self):
        """
        Test sums up contributions
        """
        range1 = ContributionRangeFactory(
            start_date=self.goal.start_date,
            end_date=self.goal_midpoint,
            user=self.user,
        )
        range2 = ContributionRangeFactory(
            start_date=self.goal_midpoint + datetime.timedelta(days=1),
            end_date=self.goal.expected_completion_date,
            user=self.user,
        )
        GoalContributionFactory(
            amount=500,
            goal=self.goal,
            percentage=100,
            date_range=range1,
        )
        GoalContributionFactory(
            amount=500,
            goal=self.goal,
            percentage=100,
            date_range=range2,
        )
        self.assertEqual(self.goal.total_contributed, 1000)

    def test_progress_as_percentage(self):
        """
        Test progress as percentage
        """
        range1 = ContributionRangeFactory(
            start_date=self.goal.start_date,
            end_date=self.goal_midpoint,
            user=self.user,
        )
        range2 = ContributionRangeFactory(
            start_date=self.goal_midpoint + datetime.timedelta(days=1),
            end_date=self.goal.expected_completion_date,
            user=self.user,
        )
        GoalContributionFactory(
            amount=self.goal.amount / 2,
            goal=self.goal,
            percentage=100,
            date_range=range1,
        )
        GoalContributionFactory(
            amount=self.goal.amount / 2,
            goal=self.goal,
            percentage=100,
            date_range=range2,
        )
        self.assertEqual(self.goal.progress, 100)

    def test_percentage_over_100(self):
        """
        Test percentage over 100
        """
        # FIXME: contributions should max out at 100% of goal
        range1 = ContributionRangeFactory(
            start_date=self.goal.start_date,
            end_date=self.goal_midpoint,
            user=self.user,
        )
        range2 = ContributionRangeFactory(
            start_date=self.goal_midpoint + datetime.timedelta(days=1),
            end_date=self.goal.expected_completion_date,
            user=self.user,
        )
        GoalContributionFactory(
            amount=self.goal.amount,
            goal=self.goal,
            percentage=100,
            date_range=range1,
        )
        GoalContributionFactory(
            amount=self.goal.amount,
            goal=self.goal,
            percentage=100,
            date_range=range2,
        )
        self.assertEqual(self.goal.progress, 200)


class TestGoalContributionModel(TestCase):
    def setUp(self):
        post_save.disconnect(sender=Goal, receiver=on_goal_create)
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def tearDown(self):
        post_save.connect(sender=Goal, receiver=on_goal_create)

    def test_cascade_deletion_of_goal(self):
        """
        Test cascade deletion of goal
        """
        goal = GoalFactory()
        contribution_range = ContributionRangeFactory(
            user=self.user,
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
        )
        GoalContributionFactory(goal=goal, date_range=contribution_range)
        self.assertEqual(goal.contributions.count(), 1)
        goal.delete()
        self.assertEqual(GoalContribution.objects.count(), 0)

    def test_percentage_must_be_between_0_and_100(self):
        """
        Test percentage must be between 0 and 100
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                percentage=101,
            )

    def test_percentage_must_be_positive(self):
        """
        Test percentage must be positive
        """
        goal = GoalFactory(
            amount=1000,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        with self.assertRaises(django.db.utils.IntegrityError):
            GoalContributionFactory(
                goal=goal,
                amount=1000,
                percentage=-1,
                date_range=range,
            )

    def test_percentage_cannot_be_over_100(self):
        """
        Test percentage cannot be over 100
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                percentage=101,
            )

    def test_cannot_have_range_before_start_date_of_goal(self):
        """
        Test cannot have range before start date of goal
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        date_range = ContributionRangeFactory(
            start_date=goal.start_date - datetime.timedelta(days=1),
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                goal=goal,
                date_range=date_range,
            )

    def test_cannot_have_range_after_end_date_of_goal(self):
        """
        Test cannot have range after end date of goal
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        date_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date + datetime.timedelta(days=1),
            user=self.user,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                goal=goal,
                date_range=date_range,
            )

    def test_percentages_over_a_range_cannot_sum_to_more_than_100(self):
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
        contribution_range = ContributionRangeFactory(
            start_date=goal1.start_date,
            end_date=goal1.expected_completion_date,
            user=self.user,
        )
        GoalContributionFactory(
            amount=1000,
            goal=goal1,
            percentage=50,
            date_range=contribution_range,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                goal=goal2,
                percentage=51,
                date_range=contribution_range,
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
        contribution_range1 = ContributionRangeFactory(
            start_date=goal1.start_date,
            end_date=goal1.expected_completion_date,
            user=self.user,
        )
        contribution_range2 = ContributionRangeFactory(
            start_date=goal2.start_date,
            end_date=goal2.expected_completion_date,
            user=user2,
        )
        GoalContributionFactory(
            amount=1000,
            goal=goal1,
            percentage=100,
            date_range=contribution_range1,
        )
        GoalContributionFactory(
            amount=1000,
            goal=goal2,
            percentage=100,
            date_range=contribution_range2,
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
            start_date=goal1.expected_completion_date + datetime.timedelta(days=1),
            expected_completion_date=goal1.expected_completion_date
            + datetime.timedelta(days=32),
            user=self.user,
        )
        contribution_range1 = ContributionRangeFactory(
            start_date=goal1.start_date,
            end_date=goal1.expected_completion_date,
            user=self.user,
        )
        contribution_range2 = ContributionRangeFactory(
            start_date=goal2.start_date,
            end_date=goal2.expected_completion_date,
            user=self.user,
        )
        GoalContributionFactory(
            amount=1000,
            goal=goal1,
            percentage=100,
            date_range=contribution_range1,
        )
        GoalContributionFactory(
            amount=1000,
            goal=goal2,
            percentage=100,
            date_range=contribution_range2,
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
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            GoalContributionFactory(
                amount=1000,
                goal=goal,
                date_range=contribution_range,
            )


class TestCalculateContributionAmount(TestCase):
    def setUp(self):
        post_save.disconnect(sender=Goal, receiver=on_goal_create)
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)
        self.goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )
        self.contribution_range = ContributionRangeFactory(
            start_date=self.goal.start_date,
            end_date=self.goal.expected_completion_date,
            user=self.user,
        )

    def tearDown(self):
        post_save.connect(sender=Goal, receiver=on_goal_create)

    def test_happy_path(self):
        """
        Test happy path
        """
        contribution = GoalContributionFactory(
            goal=self.goal,
            percentage=100,
            date_range=self.contribution_range,
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
        contribution = GoalContributionFactory(
            goal=self.goal,
            percentage=50,
            date_range=self.contribution_range,
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
        contribution = GoalContributionFactory(
            goal=self.goal,
            percentage=100,
            date_range=self.contribution_range,
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
        contribution = GoalContributionFactory(
            goal=self.goal,
            percentage=100,
            date_range=self.contribution_range,
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
            date=contribution.date_range.start_date - datetime.timedelta(days=1),
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
        contribution = GoalContributionFactory(
            goal=self.goal,
            percentage=100,
            date_range=self.contribution_range,
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
        contribution = GoalContributionFactory(
            goal=self.goal,
            percentage=100,
            amount=1000,
            date_range=self.contribution_range,
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


class TestContributionRangeModel(TestCase):
    def setUp(self):
        post_save.disconnect(sender=Goal, receiver=on_goal_create)
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)

    def tearDown(self):
        post_save.connect(sender=Goal, receiver=on_goal_create)

    def test_can_get_all_related_contributions(self):
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
        contribution_range = ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=self.user,
        )
        contribution1 = GoalContributionFactory(
            goal=goal1,
            percentage=50,
            date_range=contribution_range,
        )
        contribution2 = GoalContributionFactory(
            goal=goal2,
            percentage=50,
            date_range=contribution_range,
        )
        self.assertEqual(
            contribution_range.contributions.count(),
            2,
        )
        self.assertIn(contribution1, contribution_range.contributions.all())
        self.assertIn(contribution2, contribution_range.contributions.all())

    def test_start_date_must_be_after_end_date(self):
        """
        Test start date must be after end date
        """
        with self.assertRaises(django.core.exceptions.ValidationError):
            ContributionRangeFactory(
                start_date=self.next_year,
                end_date=self.today,
                user=self.user,
            )

    def test_cannot_have_two_overlapping_ranges_same_date(self):
        """
        Test cannot have two overlapping ranges
        """
        ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=self.user,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            ContributionRangeFactory(
                start_date=self.today,
                end_date=self.next_year,
                user=self.user,
            )

    def test_cannot_have_two_overlapping_ranges_start_date_in_range(self):
        """
        Test cannot have two overlapping ranges
        """
        ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=self.user,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            ContributionRangeFactory(
                start_date=self.today + datetime.timedelta(days=1),
                end_date=self.next_year + datetime.timedelta(days=365),
                user=self.user,
            )

    def test_cannot_have_two_overlapping_ranges_end_date_in_range(self):
        """
        Test cannot have two overlapping ranges
        """
        ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=self.user,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            ContributionRangeFactory(
                start_date=self.today - datetime.timedelta(days=1),
                end_date=self.next_year - datetime.timedelta(days=1),
                user=self.user,
            )

    def test_cannot_have_two_overlapping_ranges_start_and_end_in_range(self):
        """
        Test can have two non overlapping ranges
        """
        ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=self.user,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            ContributionRangeFactory(
                start_date=self.today + datetime.timedelta(days=1),
                end_date=self.next_year - datetime.timedelta(days=1),
                user=self.user,
            )

    def test_can_have_two_non_overlapping_ranges(self):
        """
        Test can have two non overlapping ranges
        """
        ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=self.user,
        )
        ContributionRangeFactory(
            start_date=self.next_year + datetime.timedelta(days=1),
            end_date=self.next_year + datetime.timedelta(days=32),
            user=self.user,
        )

    def test_can_have_two_overlapping_ranges_for_different_users(self):
        """
        Test can have two overlapping ranges for different users
        """
        ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=self.user,
        )
        ContributionRangeFactory(
            start_date=self.today,
            end_date=self.next_year,
            user=UserFactory(),
        )


def compare_contributions(contribution1, contribution2):
    """
    Compare contributions
    """
    return (
        contribution1.goal == contribution2.goal
        and contribution1.percentage == contribution2.percentage
        and contribution1.amount == contribution2.amount
    )


class TestAddNewRange(TestCase):
    def setUp(self):
        post_save.disconnect(sender=Goal, receiver=on_goal_create)
        self.user = UserFactory()
        self.today = datetime.date.today()

    def tearDown(self):
        post_save.connect(sender=Goal, receiver=on_goal_create)

    def test_add_new_range_no_existing_ranges(self):
        """
        Test add new range no existing ranges
        """
        ranges = ContributionRange.add_new_range(
            self.user, self.today, self.today + datetime.timedelta(days=30)
        )
        self.assertEqual(len(ranges), 1)
        new_range = ranges[0]
        self.assertEqual(ContributionRange.objects.count(), 1)
        self.assertEqual(new_range.start_date, self.today)
        self.assertEqual(new_range.end_date, self.today + datetime.timedelta(days=30))
        self.assertEqual(new_range.user, self.user)
        self.assertEqual(new_range.contributions.count(), 0)

    def test_add_new_range_case_1_1_same_as_existing_one(self):
        """
        Case 1.1: Test add new range same as existing one
        should return the existing range
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.today + datetime.timedelta(days=365),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user, goal.start_date, goal.expected_completion_date
        )
        self.assertEqual(len(ranges), 1)
        self.assertEqual(ranges[0].start_date, contribution_range.start_date)
        self.assertEqual(ranges[0].end_date, contribution_range.end_date)
        self.assertEqual(ranges[0].contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution,
                ranges[0].contributions.get(),
            )
        )

    def test_add_new_range_case_1_2_same_start_date(self):
        """
        Case 1.2: Test add new range start date is same as existing one
        end date is after.
        Should return 2 ranges
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.today + datetime.timedelta(days=365),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user, goal.start_date, goal.start_date + datetime.timedelta(days=30)
        )
        self.assertEqual(len(ranges), 2)
        new_range = ranges[0]
        self.assertEqual(new_range.start_date, goal.start_date)
        self.assertEqual(
            new_range.end_date, goal.start_date + datetime.timedelta(days=30)
        )
        self.assertEqual(new_range.user, self.user)
        self.assertEqual(new_range.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution,
                new_range.contributions.get(),
            )
        )
        old_range_shifted_right = ranges[1]
        self.assertEqual(
            old_range_shifted_right.start_date,
            goal.start_date + datetime.timedelta(days=31),
        )
        self.assertEqual(
            old_range_shifted_right.end_date, goal.expected_completion_date
        )
        self.assertEqual(old_range_shifted_right.user, self.user)
        self.assertEqual(old_range_shifted_right.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution,
                old_range_shifted_right.contributions.get(),
            )
        )

    def test_add_new_range_case_1_3_same_end_date(self):
        """
        Case 1.3: Test add new range end date is same as existing one
        start date is before.
        Should return 2 ranges
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.today + datetime.timedelta(days=365),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user,
            goal.start_date + datetime.timedelta(days=40),
            goal.expected_completion_date,
        )
        self.assertEqual(len(ranges), 2)
        old_range_shifted_left = ranges[0]
        self.assertEqual(old_range_shifted_left.start_date, goal.start_date)
        self.assertEqual(
            old_range_shifted_left.end_date,
            goal.start_date + datetime.timedelta(days=39),
        )
        self.assertEqual(old_range_shifted_left.user, self.user)
        self.assertEqual(old_range_shifted_left.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution,
                old_range_shifted_left.contributions.get(),
            )
        )
        new_range = ranges[1]
        self.assertEqual(
            new_range.start_date,
            goal.start_date + datetime.timedelta(days=40),
        )
        self.assertEqual(new_range.end_date, goal.expected_completion_date)
        self.assertEqual(new_range.user, self.user)
        self.assertEqual(new_range.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution,
                new_range.contributions.get(),
            )
        )

    def test_add_new_range_existing_range_case_1_4(self):
        """
        Case 1.4: New range is a subset of existing range
        """
        goal = GoalFactory(
            start_date=self.today - datetime.timedelta(days=365),
            expected_completion_date=self.today + datetime.timedelta(days=365),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user, self.today, self.today + datetime.timedelta(days=30)
        )
        self.assertEqual(len(ranges), 3)
        range = ranges[0]
        self.assertEqual(range.start_date, goal.start_date)
        self.assertEqual(range.end_date, self.today - datetime.timedelta(days=1))
        self.assertEqual(range.user, self.user)
        self.assertEqual(range.contributions.count(), 1)
        self.assertTrue(compare_contributions(contribution, range.contributions.get()))
        range = ranges[1]
        self.assertEqual(range.start_date, self.today)
        self.assertEqual(range.end_date, self.today + datetime.timedelta(days=30))
        self.assertEqual(range.user, self.user)
        self.assertEqual(range.contributions.count(), 1)
        self.assertTrue(compare_contributions(contribution, range.contributions.get()))
        range = ranges[2]
        self.assertEqual(range.start_date, self.today + datetime.timedelta(days=31))
        self.assertEqual(range.end_date, goal.expected_completion_date)
        self.assertEqual(range.user, self.user)
        self.assertEqual(range.contributions.count(), 1)
        self.assertTrue(compare_contributions(contribution, range.contributions.get()))

    def test_add_new_range_case_2_2_overlapping_start_eq_new_end(self):
        """
        Case 2: Overlapping range start date is eq to new range end date
        Overlapping range end date is after new range end date (obviously)
        """
        goal = GoalFactory(
            start_date=self.today + datetime.timedelta(days=40),
            expected_completion_date=self.today + datetime.timedelta(days=365),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(self.user, self.today, goal.start_date)

    def test_add_new_range_existing_range_case_2_3(self):
        """
        Case 2: Old overlapping range start date is after new range start date
        AND end date is after new range end date
        """
        goal = GoalFactory(
            start_date=self.today + datetime.timedelta(days=40),
            expected_completion_date=self.today + datetime.timedelta(days=400),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user, self.today, self.today + datetime.timedelta(days=365)
        )
        self.assertEqual(len(ranges), 3)
        new_range = ranges[0]
        self.assertEqual(new_range.start_date, self.today)
        self.assertEqual(
            new_range.end_date, goal.start_date - datetime.timedelta(days=1)
        )
        self.assertEqual(new_range.user, self.user)
        self.assertEqual(new_range.contributions.count(), 0)
        range_overlapping_old_with_new = ranges[1]
        self.assertEqual(range_overlapping_old_with_new.start_date, goal.start_date)
        self.assertEqual(
            range_overlapping_old_with_new.end_date,
            self.today + datetime.timedelta(days=365),
        )
        self.assertEqual(range_overlapping_old_with_new.user, self.user)
        self.assertEqual(range_overlapping_old_with_new.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution, range_overlapping_old_with_new.contributions.get()
            )
        )
        old_range_shifted_right = ranges[2]
        self.assertEqual(
            old_range_shifted_right.start_date,
            self.today + datetime.timedelta(days=366),
        )
        self.assertEqual(
            old_range_shifted_right.end_date, goal.expected_completion_date
        )
        self.assertEqual(old_range_shifted_right.user, self.user)

    def test_add_new_range_case_2_same_start_date(self):
        """
        Case 2: Test add new range start date is same as existing one
        end date is before.
        Should return 2 ranges
        """
        goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.today + datetime.timedelta(days=365),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user, goal.start_date, goal.start_date + datetime.timedelta(days=30)
        )
        self.assertEqual(len(ranges), 2)
        new_range = ranges[0]
        self.assertEqual(new_range.start_date, goal.start_date)
        self.assertEqual(
            new_range.end_date, goal.start_date + datetime.timedelta(days=30)
        )
        self.assertEqual(new_range.user, self.user)
        self.assertEqual(new_range.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution,
                new_range.contributions.get(),
            )
        )
        old_range_shifted_right = ranges[1]
        self.assertEqual(
            old_range_shifted_right.start_date,
            goal.start_date + datetime.timedelta(days=31),
        )
        self.assertEqual(
            old_range_shifted_right.end_date, goal.expected_completion_date
        )
        self.assertEqual(old_range_shifted_right.user, self.user)
        self.assertEqual(old_range_shifted_right.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution,
                old_range_shifted_right.contributions.get(),
            )
        )

    def test_add_new_range_existing_range_case_3(self):
        """
        Case 3: Old overlapping range start date is before new range start date
        AND end date is before new range end date
        We shift left the old range
        """
        goal = GoalFactory(
            start_date=self.today - datetime.timedelta(days=365),
            expected_completion_date=self.today + datetime.timedelta(days=30),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user, self.today, self.today + datetime.timedelta(days=365)
        )
        self.assertEqual(len(ranges), 3)
        old_range_shifted_left = ranges[0]
        self.assertEqual(old_range_shifted_left.start_date, goal.start_date)
        self.assertEqual(
            old_range_shifted_left.end_date,
            self.today - datetime.timedelta(days=1),
        )
        self.assertEqual(old_range_shifted_left.user, self.user)
        self.assertEqual(old_range_shifted_left.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution, old_range_shifted_left.contributions.get()
            )
        )
        range_overlapping_old_with_new = ranges[1]
        self.assertEqual(range_overlapping_old_with_new.start_date, self.today)
        self.assertEqual(
            range_overlapping_old_with_new.end_date,
            goal.expected_completion_date,
        )
        self.assertEqual(range_overlapping_old_with_new.user, self.user)
        self.assertEqual(range_overlapping_old_with_new.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution, range_overlapping_old_with_new.contributions.get()
            )
        )
        new_range = ranges[2]
        self.assertEqual(
            new_range.start_date, goal.expected_completion_date + datetime.timedelta(1)
        )
        self.assertEqual(new_range.end_date, self.today + datetime.timedelta(days=365))
        self.assertEqual(new_range.user, self.user)
        self.assertEqual(new_range.contributions.count(), 0)

    def test_add_new_range_existing_range_case_4(self):
        """
        Case 4: Old overlapping range is a subset of new range.
        Return old range + 2 new ranges either side of old range
        """
        goal = GoalFactory(
            start_date=self.today + datetime.timedelta(days=40),
            expected_completion_date=self.today + datetime.timedelta(days=80),
            user=self.user,
        )
        contribution_range = ContributionRangeFactory(
            start_date=goal.start_date,
            end_date=goal.expected_completion_date,
            user=self.user,
        )
        contribution = GoalContributionFactory(
            goal=goal,
            percentage=100,
            date_range=contribution_range,
        )
        ranges = ContributionRange.add_new_range(
            self.user, self.today, self.today + datetime.timedelta(days=365)
        )
        self.assertEqual(len(ranges), 3)
        new_range_left_side = ranges[0]
        self.assertEqual(new_range_left_side.start_date, self.today)
        self.assertEqual(
            new_range_left_side.end_date,
            goal.start_date - datetime.timedelta(days=1),
        )
        self.assertEqual(new_range_left_side.user, self.user)
        self.assertEqual(new_range_left_side.contributions.count(), 0)

        range_overlapping_old_with_new = ranges[1]
        self.assertEqual(range_overlapping_old_with_new.start_date, goal.start_date)
        self.assertEqual(
            range_overlapping_old_with_new.end_date,
            goal.expected_completion_date,
        )
        self.assertEqual(range_overlapping_old_with_new.user, self.user)
        self.assertEqual(range_overlapping_old_with_new.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution, range_overlapping_old_with_new.contributions.get()
            )
        )
        new_range_right_side = ranges[2]
        self.assertEqual(
            new_range_right_side.start_date,
            goal.expected_completion_date + datetime.timedelta(1),
        )
        self.assertEqual(
            new_range_right_side.end_date, self.today + datetime.timedelta(days=365)
        )
        self.assertEqual(new_range_right_side.user, self.user)
        self.assertEqual(new_range_right_side.contributions.count(), 0)

    def test_add_new_range_multiple_existing_ranges(self):
        """
        Test add new range multiple existing ranges
        One range in case 2, one range in case 3
        There is a gap between the two ranges.
        5 total ranges should be returned
        """
        goal1 = GoalFactory(
            start_date=self.today + datetime.timedelta(days=120),
            expected_completion_date=self.today + datetime.timedelta(days=400),
            user=self.user,
        )
        contribution_range1 = ContributionRangeFactory(
            start_date=goal1.start_date,
            end_date=goal1.expected_completion_date,
            user=self.user,
        )
        contribution1 = GoalContributionFactory(
            goal=goal1,
            percentage=100,
            date_range=contribution_range1,
        )
        goal2 = GoalFactory(
            start_date=self.today - datetime.timedelta(days=365),
            expected_completion_date=self.today + datetime.timedelta(days=40),
            user=self.user,
        )
        contribution_range2 = ContributionRangeFactory(
            start_date=goal2.start_date,
            end_date=goal2.expected_completion_date,
            user=self.user,
        )
        contribution2 = GoalContributionFactory(
            goal=goal2,
            percentage=100,
            date_range=contribution_range2,
        )
        ranges = ContributionRange.add_new_range(
            self.user, self.today, self.today + datetime.timedelta(days=365)
        )
        self.assertEqual(len(ranges), 5)
        goal2_left_side_range = ranges[0]
        self.assertEqual(goal2_left_side_range.start_date, goal2.start_date)
        self.assertEqual(
            goal2_left_side_range.end_date,
            self.today - datetime.timedelta(days=1),
        )
        self.assertEqual(goal2_left_side_range.user, self.user)
        self.assertEqual(goal2_left_side_range.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution2, goal2_left_side_range.contributions.get()
            )
        )

        goal2_range_overlapping_old_with_new = ranges[1]
        self.assertEqual(goal2_range_overlapping_old_with_new.start_date, self.today)
        self.assertEqual(
            goal2_range_overlapping_old_with_new.end_date,
            goal2.expected_completion_date,
        )
        self.assertEqual(goal2_range_overlapping_old_with_new.user, self.user)
        self.assertEqual(goal2_range_overlapping_old_with_new.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution2,
                goal2_range_overlapping_old_with_new.contributions.get(),
            )
        )
        new_range_no_overlaps = ranges[2]
        self.assertEqual(
            new_range_no_overlaps.start_date,
            goal2.expected_completion_date + datetime.timedelta(1),
        )
        self.assertEqual(
            new_range_no_overlaps.end_date,
            goal1.start_date - datetime.timedelta(days=1),
        )
        self.assertEqual(new_range_no_overlaps.user, self.user)
        self.assertEqual(new_range_no_overlaps.contributions.count(), 0)

        goal1_range_overlapping_old_with_new = ranges[3]
        self.assertEqual(
            goal1_range_overlapping_old_with_new.start_date, goal1.start_date
        )
        self.assertEqual(
            goal1_range_overlapping_old_with_new.end_date,
            self.today + datetime.timedelta(days=365),
        )
        self.assertEqual(goal1_range_overlapping_old_with_new.user, self.user)
        self.assertEqual(goal1_range_overlapping_old_with_new.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution1,
                goal1_range_overlapping_old_with_new.contributions.get(),
            )
        )

        goal1_right_side_range = ranges[4]
        self.assertEqual(
            goal1_right_side_range.start_date, self.today + datetime.timedelta(days=366)
        )
        self.assertEqual(
            goal1_right_side_range.end_date, goal1.expected_completion_date
        )
        self.assertEqual(goal1_right_side_range.user, self.user)
        self.assertEqual(goal1_right_side_range.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution1,
                goal1_right_side_range.contributions.get(),
            )
        )

    def test_add_new_range_multiple_existing_ranges_no_gap(self):
        """
        Test add new range multiple existing ranges
        One range in case 2, one range in case 3
        No gap between the two ranges.
        4 total ranges should be returned
        """
        goal1 = GoalFactory(
            start_date=self.today + datetime.timedelta(days=40),
            expected_completion_date=self.today + datetime.timedelta(days=400),
            user=self.user,
        )
        contribution_range1 = ContributionRangeFactory(
            start_date=goal1.start_date,
            end_date=goal1.expected_completion_date,
            user=self.user,
        )
        contribution1 = GoalContributionFactory(
            goal=goal1,
            percentage=100,
            date_range=contribution_range1,
        )
        goal2 = GoalFactory(
            start_date=self.today - datetime.timedelta(days=365),
            expected_completion_date=goal1.start_date - datetime.timedelta(days=1),
            user=self.user,
        )
        contribution_range2 = ContributionRangeFactory(
            start_date=goal2.start_date,
            end_date=goal2.expected_completion_date,
            user=self.user,
        )
        contribution2 = GoalContributionFactory(
            goal=goal2,
            percentage=100,
            date_range=contribution_range2,
        )
        ranges = ContributionRange.add_new_range(
            self.user, self.today, self.today + datetime.timedelta(days=365)
        )
        self.assertEqual(len(ranges), 4)
        goal2_left_side_range = ranges[0]
        self.assertEqual(goal2_left_side_range.start_date, goal2.start_date)
        self.assertEqual(
            goal2_left_side_range.end_date,
            self.today - datetime.timedelta(days=1),
        )
        self.assertEqual(goal2_left_side_range.user, self.user)
        self.assertEqual(goal2_left_side_range.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution2, goal2_left_side_range.contributions.get()
            )
        )

        goal2_range_overlapping_old_with_new = ranges[1]
        self.assertEqual(goal2_range_overlapping_old_with_new.start_date, self.today)
        self.assertEqual(
            goal2_range_overlapping_old_with_new.end_date,
            goal2.expected_completion_date,
        )
        self.assertEqual(goal2_range_overlapping_old_with_new.user, self.user)
        self.assertEqual(goal2_range_overlapping_old_with_new.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution2,
                goal2_range_overlapping_old_with_new.contributions.get(),
            )
        )
        goal1_range_overlapping_old_with_new = ranges[2]
        self.assertEqual(
            goal1_range_overlapping_old_with_new.start_date, goal1.start_date
        )
        self.assertEqual(
            goal1_range_overlapping_old_with_new.end_date,
            self.today + datetime.timedelta(days=365),
        )
        self.assertEqual(goal1_range_overlapping_old_with_new.user, self.user)
        self.assertEqual(goal1_range_overlapping_old_with_new.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution1,
                goal1_range_overlapping_old_with_new.contributions.get(),
            )
        )

        goal1_right_side_range = ranges[3]
        self.assertEqual(
            goal1_right_side_range.start_date, self.today + datetime.timedelta(days=366)
        )
        self.assertEqual(
            goal1_right_side_range.end_date, goal1.expected_completion_date
        )
        self.assertEqual(goal1_right_side_range.user, self.user)
        self.assertEqual(goal1_right_side_range.contributions.count(), 1)
        self.assertTrue(
            compare_contributions(
                contribution1,
                goal1_right_side_range.contributions.get(),
            )
        )


class TestUpdateContributions(TestCase):
    def setUp(self):
        # keep signals
        self.user = UserFactory()
        self.today = datetime.date.today()
        self.next_year = self.today.replace(year=self.today.year + 1)
        self.goal = GoalFactory(
            start_date=self.today,
            expected_completion_date=self.next_year,
            user=self.user,
        )

    @staticmethod
    def create_contribution(goal, start_date, end_date, user, percentage=100):
        contribution_range = ContributionRangeFactory(
            start_date=start_date,
            end_date=end_date,
            user=user,
        )
        return GoalContributionFactory(
            goal=goal,
            percentage=percentage,
            date_range=contribution_range,
        )

    def test_update_contributions(self):
        """
        Test update contributions
        """
        goal2 = GoalFactory(
            start_date=self.goal.start_date,
            expected_completion_date=self.goal.expected_completion_date,
            user=self.user,
        )
        contribution_range = ContributionRange.objects.get()
        goal_contribution = self.goal.contributions.get()
        goal2_contribution = goal2.contributions.get()
        self.assertEqual(goal_contribution.percentage, 100)
        self.assertEqual(goal2_contribution.percentage, 0)
        self.assertEqual(contribution_range.contributions.count(), 2)

        # update goal 2 to be 50% of the range
        contribution_range.update_contributions(
            [
                {
                    "goal": GoalSmallSerializer(goal2).data,
                    "percentage": 50,
                    "amount": 200,
                },
                {
                    "goal": GoalSmallSerializer(self.goal).data,
                    "percentage": 50,
                    "amount": 100,
                },
            ]
        )
        self.goal.refresh_from_db(), goal2.refresh_from_db()
        goal_contribution = self.goal.contributions.get()
        goal2_contribution = goal2.contributions.get()
        self.assertEqual(goal_contribution.percentage, 50)
        self.assertEqual(goal2_contribution.percentage, 50)
        self.assertEqual(contribution_range.contributions.count(), 2)
        self.assertEqual(goal2_contribution.amount, 200)
        self.assertEqual(goal_contribution.amount, 100)

    def test_update_contributions_percentage_over_100(self):
        """
        Test update contributions
        """
        goal2 = GoalFactory(
            start_date=self.goal.start_date,
            expected_completion_date=self.goal.expected_completion_date,
            user=self.user,
        )
        contribution_range = ContributionRange.objects.get()
        goal_contribution = self.goal.contributions.get()
        goal2_contribution = goal2.contributions.get()
        self.assertEqual(goal_contribution.percentage, 100)
        self.assertEqual(goal2_contribution.percentage, 0)
        self.assertEqual(contribution_range.contributions.count(), 2)

        with self.assertRaises(django.core.exceptions.ValidationError):
            # update goal 2 to be 50% of the range
            contribution_range.update_contributions(
                [
                    {
                        "goal": GoalSmallSerializer(goal2).data,
                        "percentage": 100,
                        "amount": 200,
                    },
                    {
                        "goal": GoalSmallSerializer(self.goal).data,
                        "percentage": 50,
                        "amount": 100,
                    },
                ]
            )
        self.goal.refresh_from_db(), goal2.refresh_from_db()
        goal_contribution = self.goal.contributions.get()
        goal2_contribution = goal2.contributions.get()
        self.assertEqual(goal_contribution.percentage, 100)
        self.assertEqual(goal2_contribution.percentage, 0)
        self.assertEqual(contribution_range.contributions.count(), 2)