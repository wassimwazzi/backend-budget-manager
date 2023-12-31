from celery import shared_task
from transaction.models import Transaction
from category.models import Category
from django.db import transaction as db_transaction
from django.contrib.auth.models import User
from inference.inference import infer_categories
import pandas as pd

# FIXME: Uncomment to add celery task back
# @shared_task
def infer_categories_task(user_id, webhook_url=None):
    user = User.objects.get(id=user_id)
    transactions = Transaction.objects.filter(user=user, inferred_category=True)
    infer_categories(transactions, user)
    return True
