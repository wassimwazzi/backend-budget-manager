"""
Signals for category app
"""

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from category.models import Category

INCOME_CATEGORIES = [
    ("Salary", True, "Salary", False),
    ("Reimbursement", True, "E.g. Taxes", False),
    ("Other Income", True, "No specific category", True),
]

EXPENSE_CATEGORIES = [
    ("Shopping", False, "Shopping", False),
    ("Depanneur", False, "Convenience store", False),
    ("Education", False, "Education", False),
    ("Entertainment", False, "Entertainment", False),
    ("Fast Food", False, "Any food to go / fast food", False),
    ("Fees", False, "Any fees or unexpected payments", False),
    ("Food Delivery", False, "", False),
    ("Gifts", False, "Gifts", False),
    ("Groceries", False, "Groceries", False),
    ("Health Care", False, "Health, beauty, massage, etc.", False),
    ("Home", False, "Items for home", False),
    ("Investments", False, "Investments", False),
    ("Other Expense", False, "No specific category", True),
    ("Restaurants", False, "", False),
    ("Self Care", False, "Health, beauty, massage, etc.", False),
    ("Sports", False, "Sports", False),
    ("Subscriptions", False, "Subscriptions, e.g. Netflix", False),
    ("Transportation", False, "Transportation", False),
    ("Travel", False, "Travel", False),
    ("Utilities", False, "Utilities", False),
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
            is_default=category[3],
            user=instance,
        )
