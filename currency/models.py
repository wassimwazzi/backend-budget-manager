"""
Currency Model
"""
from django.db import models


class Currency(models.Model):
    """
    Currency Model
    """

    code = models.CharField(primary_key=True, max_length=3)

    class Meta:
        """
        Meta class for Currency
        """

        verbose_name_plural = "currencies"
