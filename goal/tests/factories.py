import factory
import factory.fuzzy
from users.user_factory import UserFactory
from ..models import (
    Goal,
    GoalContribution,
    GoalType,
    GoalStatus,
    GoalRecurranceType,
    ContributionRange,
)
import datetime


class GoalFactory(factory.django.DjangoModelFactory):
    """
    Goal factory
    """

    class Meta:
        model = Goal

    amount = factory.Faker("pyint")
    # future date
    expected_completion_date = factory.fuzzy.FuzzyDate(
        datetime.date.today() + datetime.timedelta(days=1),
        datetime.date.today().replace(day=1) + datetime.timedelta(days=365),
    )
    type = GoalType.SAVINGS
    description = factory.Faker("sentence")
    status = GoalStatus.PENDING
    start_date = None
    recurring = GoalRecurranceType.NON_RECURRING
    reccuring_frequency = None
    previous_goal = None
    user = factory.SubFactory(UserFactory)


class ContributionRangeFactory(factory.django.DjangoModelFactory):
    """
    Contribution range factory
    """

    class Meta:
        model = ContributionRange

    user = factory.SubFactory(UserFactory)
    start_date = factory.fuzzy.FuzzyDate(
        datetime.date.today() + datetime.timedelta(days=1),
        datetime.date.today().replace(day=1) + datetime.timedelta(days=365),
    )
    end_date = factory.fuzzy.FuzzyDate(
        datetime.date.today() + datetime.timedelta(days=31),
        datetime.date.today().replace(day=1) + datetime.timedelta(days=365),
    )


class GoalContributionFactory(factory.django.DjangoModelFactory):
    """
    Goal contribution factory
    """

    class Meta:
        model = GoalContribution

    amount = None
    goal = factory.SubFactory(
        GoalFactory, start_date=datetime.date.today().replace(day=1)
    )
    percentage = factory.fuzzy.FuzzyInteger(0, 100)
    date_range = factory.SubFactory(ContributionRangeFactory)