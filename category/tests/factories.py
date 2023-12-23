import factory
from user_factory import UserFactory
from ..models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    Category factory
    """

    class Meta:
        model = Category

    category = factory.Sequence(lambda n: f"Category {n}")
    income = factory.Faker("boolean")
    description = factory.Faker("sentence")
    user = factory.SubFactory(UserFactory)
