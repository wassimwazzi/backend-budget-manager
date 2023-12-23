import factory
from user_factory import UserFactory
from category.tests.factories import CategoryFactory
from currency.tests.factories import CurrencyFactory
from ..models import Budget


class BudgetFactory(factory.django.DjangoModelFactory):
    """
    Budget factory
    """

    class Meta:
        model = Budget

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory, user=factory.SelfAttribute("..user"))
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    currency = factory.SubFactory(CurrencyFactory)
    start_date = factory.Faker("date_this_month")
