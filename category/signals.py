"""
Signals for category app
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from category.models import Category

INCOME_CATEGORIES = [
    ("Salary", True, "Salary"),
    ("Reimbursement", True, "E.g. Taxes"),
]

EXPENSE_CATEGORIES = [
    ("Clothing", False, "Clothing"),
    ("Depanneur", False, "Convenience store"),
    ("Education", False, "Education"),
    ("Entertainment", False, "Entertainment"),
    ("Fast Food", False, "Any food to go / fast food"),
    ("Fees", False, "Any fees or unexpected payments"),
    ("Food Delivery", False, ""),
    ("Gifts", False, "Gifts"),
    ("Groceries", False, "Groceries"),
    ("Health Care", False, "Health, beauty, massage, etc."),
    ("Home", False, "Items for home"),
    ("Investments", False, "Investments"),
    ("Other", False, "No specific category"),
    ("Restaurants", False, ""),
    ("Self Care", False, "Health, beauty, massage, etc."),
    ("Sports", False, "Sports"),
    ("Subscriptions", False, "Subscriptions, e.g. Netflix"),
    ("Transportation", False, "Transportation"),
    ("Travel", False, "Travel"),
    ("Utilities", False, "Utilities"),
]

DEFAULT_CATEGORIES = INCOME_CATEGORIES + EXPENSE_CATEGORIES


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
