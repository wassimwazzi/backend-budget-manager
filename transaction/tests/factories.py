import factory
from users.user_factory import UserFactory
from category.tests.factories import CategoryFactory
from currency.tests.factories import CurrencyFactory
from plaidapp.tests.factories import PlaidTransactionFactory
from ..models import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    """
    Transaction factory
    """

    class Meta:
        model = Transaction

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory, user=factory.SelfAttribute("..user"))
    plaid_transaction = factory.SubFactory(PlaidTransactionFactory)
    amount = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    currency = factory.SubFactory(CurrencyFactory)
    date = factory.Faker("date_this_month")
    description = factory.Faker("sentence")
    code = factory.Faker("ean13")
    inferred_category = factory.Faker("boolean")
    file = None
