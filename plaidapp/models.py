from django.db import models
from django.contrib.auth.models import User


class PlaidItem(models.Model):
    item_id = models.CharField(max_length=255, primary_key=True)
    access_token = models.CharField(max_length=255)
    institution_id = models.CharField(max_length=255)
    institution_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    max_lookback_days = models.IntegerField(null=True, blank=True)
    last_cursor = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.institution_name} - {self.user}"

    class Meta:
        verbose_name = "Plaid Item"
        verbose_name_plural = "Plaid Items"
        unique_together = ["item_id", "user"]


class PlaidItemSync(models.Model):
    item = models.ForeignKey(PlaidItem, on_delete=models.CASCADE)
    last_synced = models.DateTimeField()
    last_failed = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.IntegerField(default=0)
    cursor = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.item} - {self.last_synced}"

    class Meta:
        verbose_name = "Plaid Item Sync"
        verbose_name_plural = "Plaid Item Syncs"
        unique_together = ["item", "cursor"]


class PlaidAccount(models.Model):
    item = models.ForeignKey(PlaidItem, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=255, primary_key=True)
    mask = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255, null=True, blank=True)
    subtype = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255)
    iso_currency_code = models.CharField(max_length=3, null=True, blank=True)
    available_balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    current_balance = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_lookback_days = models.IntegerField(
        null=True, blank=True
    )  # Override the PlaidItem max_lookback_days

    def __str__(self):
        return f"{self.name} - {self.item}"

    class Meta:
        verbose_name = "Plaid Account"
        verbose_name_plural = "Plaid Accounts"


class Location(models.Model):
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(
        max_length=2, null=True, blank=True
    )  # ISO 3166-1 alpha-2 country code

    def __str__(self):
        return f"{self.address} - {self.city}, {self.region} {self.postal_code} {self.country}"

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class TransactionStatus(models.TextChoices):
    REMOVED = "REMOVED", "Removed"
    ADDED = "ADDED", "Added"
    MODIFIED = "MODIFIED", "Modified"


class PlaidTransaction(models.Model):
    # item = models.ForeignKey(PlaidItem, on_delete=models.CASCADE)
    item_sync = models.ForeignKey(PlaidItemSync, on_delete=models.CASCADE)
    account = models.ForeignKey(PlaidAccount, on_delete=models.CASCADE)
    plaid_transaction_id = models.CharField(max_length=255)
    # foreign key is on the transaction model
    # transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    category_id = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True
    )
    # merchant name here, and name saved as description in transaction model
    name = models.CharField(max_length=255, null=True, blank=True)
    pending = models.BooleanField()
    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.ADDED,
    )
    # description = models.TextField(null=True, blank=True)
