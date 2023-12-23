"""
Transactions model
"""
from django.utils import timezone
from category.models import Category
from currency.models import Currency
from fileupload.models import FileUpload
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Transaction(models.Model):
    """
    Transactions model
    """

    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default="CAD")
    date = models.DateField()
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    inferred_category = models.BooleanField(default=False)
    file = models.ForeignKey(
        FileUpload, on_delete=models.PROTECT, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.code}: {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        # validate date is not in the future
        if self.date > timezone.now().date():
            raise ValidationError("Date cannot be in the future")
        super().save(*args, **kwargs)
