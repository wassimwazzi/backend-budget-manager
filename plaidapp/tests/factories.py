import factory
import factory.fuzzy
from users.user_factory import UserFactory
from ..models import (
    PlaidAccount,
    PlaidItem,
    PlaidItemSync,
    PlaidTransaction,
    Location,
)


class PlaidItemFactory(factory.django.DjangoModelFactory):
    """
    PlaidItem factory
    """

    class Meta:
        model = PlaidItem

    item_id = factory.Faker("uuid4")
    access_token = factory.Faker("uuid4")
    institution_id = factory.Faker("uuid4")
    institution_name = factory.Faker("company")
    user = factory.SubFactory(UserFactory)
    max_lookback_date = None
    last_cursor = None


class PlaidItemSyncFactory(factory.django.DjangoModelFactory):
    """
    PlaidItemSync factory
    """

    class Meta:
        model = PlaidItemSync

    item = factory.SubFactory(PlaidItemFactory)
    last_synced = factory.Faker("date_time_this_month")
    last_failed = None
    failed_attempts = 0
    cursor = factory.Faker("uuid4")


class PlaidAccountFactory(factory.django.DjangoModelFactory):
    """
    PlaidAccount factory
    """

    class Meta:
        model = PlaidAccount

    item = factory.SubFactory(PlaidItemFactory)
    account_id = factory.Faker("uuid4")
    mask = factory.Faker("credit_card_number")
    name = factory.Faker("word")
    official_name = None
    subtype = None
    type = factory.Faker("word")
    iso_currency_code = factory.Faker("currency_code")
    available_balance = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    current_balance = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )
    limit = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    max_lookback_date = None


class LocationFactory(factory.django.DjangoModelFactory):
    """
    Location factory
    """

    class Meta:
        model = Location

    address = factory.Faker("street_address")
    city = factory.Faker("city")
    region = factory.Faker("state")
    postal_code = factory.Faker("postcode")
    country = factory.Faker("country")


class PlaidTransactionFactory(factory.django.DjangoModelFactory):
    """
    PlaidTransaction factory
    """

    class Meta:
        model = PlaidTransaction

    item_sync = factory.SubFactory(PlaidItemSyncFactory)
    account = factory.SubFactory(PlaidAccountFactory)
    plaid_transaction_id = factory.Faker("uuid4")
    category = factory.Faker("word")
    category_id = factory.Faker("uuid4")
    location = factory.SubFactory(LocationFactory)
    name = factory.Faker("word")
    pending = factory.Faker("boolean")
    status = factory.Faker("random_element", elements=["REMOVED", "ADDED", "MODIFIED"])
