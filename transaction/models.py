"""
Transactions model
"""

from django.utils import timezone
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from category.models import Category
from currency.models import Currency
from plaidapp.models import PlaidTransaction
from fileupload.models import FileUpload
from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    """
    Transactions model
    """

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default="CAD")
    date = models.DateField()
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    inferred_category = models.BooleanField(default=False)
    file = models.ForeignKey(
        FileUpload, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plaid_transaction = models.ForeignKey(
        PlaidTransaction, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.date} - {self.code}: {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # convert date to date field
        if isinstance(self.date, str):
            self.date = timezone.datetime.strptime(self.date, "%Y-%m-%d").date()
        # validate date is not in the future
        if self.date > timezone.now().date():
            raise IntegrityError("Date cannot be in the future")
        # Validate that the category is the correct user
        if self.category.user != self.user:
            raise IntegrityError("Category must belong to the user")
        # validate code and description are not both null
        if not self.code and not self.description:
            raise IntegrityError("Code and description cannot both be null")
        # validate that the amount is larger than 0
        if self.amount <= 0:
            raise IntegrityError("Amount must be larger than 0")
