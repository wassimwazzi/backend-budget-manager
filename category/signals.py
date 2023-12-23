"""
Signals for category app
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from category.models import Category

DEFAULT_CATEGORIES = [
    ("Salary", True, "Salary"),
    ("Reimbursment", True, "E.g. Taxes"),
    ("Home", False, "Items for home"),
    ("Utilities", False, "Utilities"),
    ("Fast Food", False, "Any food to go / fast food"),
    ("Food Delivery", False, ""),
    ("Depanneur", False, "Convenience store"),
    ("Restaurants", False, ""),
    ("Groceries", False, "Groceries"),
    ("Subscriptions", False, "Subscriptions, e.g. Netflix"),
    ("Fees", False, "Any fees or unexpected payments"),
    ("Transportation", False, "Transportation"),
    ("Entertainment", False, "Entertainment"),
    ("Clothing", False, "Clothing"),
    ("Education", False, "Education"),
    ("Gifts", False, "Gifts"),
    ("Self Care", False, "Health, beauty, massage, etc."),
    ("Travel", False, "Travel"),
    ("Investments", False, "Investments"),
    ("Other", False, "No specific category"),
]


@receiver(post_save, sender=User)
def on_user_created(sender, instance, created, **kwargs):
    """
    Create default categories for user
    """
    if not created:
        return

    for category in DEFAULT_CATEGORIES:
        Category.objects.create(
            category=category[0],
            income=category[1],
            description=category[2],
            user=instance,
        )
