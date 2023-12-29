import factory
import factory.fuzzy
from users.user_factory import UserFactory
from ..models import Goal, GoalContribution, GoalType, GoalStatus, GoalRecurranceType
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


class GoalContributionFactory(factory.django.DjangoModelFactory):
    """
    Goal contribution factory
    """

    class Meta:
        model = GoalContribution

    amount = factory.Faker("pyint")
    goal = factory.SubFactory(GoalFactory, start_date=datetime.date.today().replace(day=1))
    percentage = factory.fuzzy.FuzzyInteger(0, 100)

    @factory.lazy_attribute
    def start_date(self):
        # Check if the goal already has a contribution
        existing_contributions = GoalContribution.objects.filter(goal=self.goal)

        if existing_contributions.exists():
            # Increment the start_date to the next month
            last_contribution = existing_contributions.latest("start_date")
            next_month_start_date = (
                last_contribution.start_date.replace(day=1) + datetime.timedelta(days=32)
            ).replace(day=1)

            return next_month_start_date
        else:
            # default to goal start date
            return self.goal.start_date
