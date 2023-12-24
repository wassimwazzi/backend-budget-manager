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
    is_default = models.BooleanField(default=False)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category}: {self.description}"

    def save(self, *args, **kwargs):
        """
        Save category
        """
        if self.is_default:
            if Category.objects.filter(
                user=self.user, is_default=True, income=self.income
            ).exists():
                raise Exception("Cannot have multiple default categories")
        super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete category
        """
        if self.is_default:
            raise Exception("Cannot delete default category")
        super(Category, self).delete(*args, **kwargs)

    class Meta:
        """
        Meta class for Category
        """

        verbose_name_plural = "Categories"
        unique_together = ["category", "user"]
