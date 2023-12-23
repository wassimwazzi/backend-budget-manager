"""
Category Model
"""
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Category Model
    """

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20)
    income = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category}: {self.description}"

    class Meta:
        """
        Meta class for Category
        """

        verbose_name_plural = "Categories"
        unique_together = ["category", "user"]
