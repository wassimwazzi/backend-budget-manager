from celery import shared_task
from transaction.models import Transaction
from category.models import Category
from django.db import transaction as db_transaction
from django.contrib.auth.models import User
import requests
import inference
import pandas as pd


@shared_task
def infer_categories_task(user_id, webhook_url=None):
    user = User.objects.get(id=user_id)
    print("Infering categories for user", user)
    transactions = Transaction.objects.filter(
        user=user, inferred_category=True
    ).exclude(category__category="Other")
    transactions_df = pd.DataFrame(
        transactions.values_list("id", "description", "code", "category__category"),
        columns=["id", "Description", "Code", "Category"],
    )

    categories = (
        Category.objects.filter(user=user)
        .values_list("category", flat=True)
        .exclude(category="Other")
    )
    # infer_categories modifies the dataframe in place
    transactions_df = inference.infer_categories(transactions_df, categories)

    with db_transaction.atomic():
        for index, row in transactions_df.iterrows():
            transaction = Transaction.objects.get(id=row["id"])
            transaction.category = Category.objects.get(category=row["Category"])
            transaction.save()

        if webhook_url:
            requests.post(webhook_url, json={"message": "Inferred categories"})

    return True
