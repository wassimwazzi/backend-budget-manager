import factory
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    User factory
    """

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User {n}")
    email = factory.Faker("email")
    password = factory.Faker("password")
