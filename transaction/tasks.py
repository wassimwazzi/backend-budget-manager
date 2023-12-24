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
    transactions = Transaction.objects.filter(user=user, inferred_category=True)
    transactions_df = pd.DataFrame(
        transactions.values_list("id", "description", "code", "category__category"),
        columns=["id", "description", "code", "category"],
    )

    income_categories = Category.objects.filter(user=user, income=True).values_list(
        "category", flat=True
    )
    expense_categories = Category.objects.filter(user=user, income=False).values_list(
        "category", flat=True
    )
    default_income_category = Category.objects.get(
        user=user, income=True, is_default=True
    ).category
    default_expense_category = Category.objects.get(
        user=user, income=False, is_default=True
    ).category
    income_df = transactions_df[transactions_df["income"] > 0]
    expense_df = transactions_df[transactions_df["expense"] > 0]

    # infer categories
    income_df = inference.infer_categories(
        income_df, income_categories, default_income_category
    )
    expense_df = inference.infer_categories(
        expense_df, expense_categories, default_expense_category
    )
    # combine dataframes
    transactions_df = pd.concat([income_df, expense_df])

    with db_transaction.atomic():
        for index, row in transactions_df.iterrows():
            transaction = Transaction.objects.get(id=row["id"])
            transaction.category = Category.objects.get(category=row["category"])
            transaction.save()

        if webhook_url:
            requests.post(webhook_url, json={"message": "Inferred categories"})

    return True
