from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PlaidItem(models.Model):
    item_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    institution_id = models.CharField(max_length=255)
    institution_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.institution_name} - {self.user}"
    
    class Meta:
        verbose_name = "Plaid Item"
        verbose_name_plural = "Plaid Items"
        unique_together = ["item_id", "user"]
