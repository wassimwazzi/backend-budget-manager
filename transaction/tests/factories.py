import factory
from user_factory import UserFactory
from category.tests.factories import CategoryFactory
from currency.tests.factories import CurrencyFactory
from ..models import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    """
    Transaction factory
    """

    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory, user=factory.SelfAttribute("..user"))
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    currency = factory.SubFactory(CurrencyFactory)
    date = factory.Faker("date_this_month")
    description = factory.Faker("sentence")
    code = factory.Faker("ean13")
    inferred_category = factory.Faker("boolean")
    file = None
