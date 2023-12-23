import factory
from ..models import Currency


class CurrencyFactory(factory.django.DjangoModelFactory):
    """
    Currency factory
    """

    class Meta:
        model = Currency

    code = factory.Sequence(lambda n: f"Currency {n}")
