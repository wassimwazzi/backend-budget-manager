from celery import shared_task
from transaction.models import Transaction
from category.models import Category
from .models import FileUpload, Status
from django.db import transaction as db_transaction
import django.core.exceptions
from datetime import datetime
import pandas as pd
from inference import infer_categories
import math


def sanitize_df(df, categories):
    df.columns = df.columns.str.strip().str.lower()
    error_msg = ""
    # validate column names
    expected_columns = ["date", "description", "category", "code", "income", "expense"]
    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        error_msg += f"Missing columns: {', '.join(missing_cols)}\n"
    convert_amount = (
        lambda x: (float(x.replace(",", "")) if x else x) if isinstance(x, str) else x
    )
    round_amount = lambda x: round(x, 2) if x else x
    df["income"] = df["income"].apply(convert_amount).apply(round_amount)
    df["expense"] = df["expense"].apply(convert_amount).apply(round_amount)

    # validate no row has null income and expense
    invalid_amounts = df[
        (df["income"].isnull()) & (df["expense"].isnull())
        | (df["income"] == 0) & (df["expense"] == 0)
    ]
    if not invalid_amounts.empty:
        row_numbers = [index + 1 for index in invalid_amounts.index.tolist()]
        error_msg += f"rows {row_numbers} do not have income or expense\n"
    # Validate no row has both income and expense
    invalid_amounts = df[
        (
            (df["income"].notnull() & (df["income"] > 0))
            & ((df["expense"].notnull()) & (df["expense"] > 0))
        )
    ]
    if not invalid_amounts.empty:
        row_numbers = [index + 1 for index in invalid_amounts.index.tolist()]
        error_msg += f"rows {row_numbers} have both income and expense\n"
    # validate income/expense: No negative income/expense
    invalid_amounts = df[
        (
            (df["income"].notnull() & (df["income"] <= 0))
            | ((df["expense"].notnull()) & (df["expense"] <= 0))
        )
    ]
    if not invalid_amounts.empty:
        row_numbers = [index + 1 for index in invalid_amounts.index.tolist()]
        error_msg += f"Income or expense is negative or 0 in rows {row_numbers}\n"
    try:
        df["date"] = pd.to_datetime(df["date"], format="mixed", dayfirst=False).dt.date
    except Exception as e:
        print(e)
        error_msg += "Invalid date format: must be YYYY-MM-DD\n"
        return error_msg, df

    # validate date
    today = datetime.today().date()
    future_dates = df[df["date"] > today]
    if not future_dates.empty:
        row_numbers = [index + 1 for index in future_dates.index.tolist()]
        error_msg += f"rows {row_numbers} have dates in the future\n"

    df["code"] = df["code"].apply(lambda x: str(x).strip() if not pd.isnull(x) else "")
    df["category"] = df["category"].apply(
        lambda x: str(x).title().strip() if not pd.isnull(x) else ""
    )
    # convert nan descriptions to empty string
    df["description"] = df["description"].apply(
        lambda x: str(x).strip() if not pd.isnull(x) else ""
    )
    # Validate no row has empty description and code
    invalid_rows = df[(df["description"] == "") & (df["code"] == "")]
    if not invalid_rows.empty:
        row_numbers = [index + 1 for index in invalid_rows.index.tolist()]
        error_msg += f"rows {row_numbers} have empty description and code\n"
    # validate categories
    income_categories = df[df["income"] > 0]["category"].unique()
    expense_categories = df[df["expense"] > 0]["category"].unique()
    existing_income_categories = categories.filter(income=True).values_list(
        "category", flat=True
    )
    existing_expense_categories = categories.filter(income=False).values_list(
        "category", flat=True
    )
    missing_income_categories = [
        category
        for category in income_categories
        if category and category not in existing_income_categories
    ]
    missing_expense_categories = [
        category
        for category in expense_categories
        if category and category not in existing_expense_categories
    ]
    if missing_income_categories:
        error_msg += f"These income categories do not exist: {', '.join(missing_income_categories)}\n"
    if missing_expense_categories:
        error_msg += f"These expense categories do not exist: {', '.join(missing_expense_categories)}\n"

    return error_msg, df


def create_transactions(df, instance, categories):
    try:
        with db_transaction.atomic():
            for index, row in df.iterrows():
                default_category = (
                    categories.get(income=True, is_default=True).category
                    if not math.isnan(row["income"])
                    else categories.get(income=False, is_default=True).category
                )
                category = (
                    categories.get(category=row["category"])
                    if row["category"]
                    else categories.get(category=default_category)
                )
                amount = (
                    row["income"] if not math.isnan(row["income"]) else row["expense"]
                )
                Transaction.objects.create(
                    date=row["date"],
                    description=row["description"],
                    amount=amount,
                    category=category,
                    code=row["code"],
                    file=instance,
                    inferred_category=False,
                    user=instance.user,
                )
    except django.core.exceptions.ValidationError as e:
        return str(e)


@shared_task
def process_file(fileupload_id):
    """
    Process file after upload
    """
    instance = FileUpload.objects.get(id=fileupload_id)

    try:
        with open(instance.file.path, "r", encoding="utf-8") as f:
            instance.status = Status.IN_PROGRESS
            df = pd.read_csv(f)
            categories = Category.objects.filter(user=instance.user)
            error_msg, df = sanitize_df(df, categories)
            if error_msg:
                instance.status = Status.FAILED
                instance.message = error_msg
                instance.save()
                return False
            error_msg = create_transactions(df, instance, categories)
            if error_msg:
                instance.status = Status.FAILED
                instance.message = error_msg
                instance.save()
                return False
            transactions = Transaction.objects.filter(
                file=instance, inferred_category=True
            )
            infer_categories(transactions, instance.user)
            instance.status = Status.COMPLETED
            instance.save()
            return True

    except Exception:
        import traceback

        traceback.print_exc()

        instance.status = Status.FAILED
        instance.message = "Error processing file"
        instance.save()
        return False

