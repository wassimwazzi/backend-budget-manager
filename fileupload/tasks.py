from celery import shared_task
from transaction.models import Transaction
from category.models import Category
from .models import FileUpload, Status
from django.db import transaction as db_transaction
from datetime import datetime
import pandas as pd
from inference import infer_categories


def sanitize_df(df, categories):
    df.columns = df.columns.str.strip().str.lower()
    error_msg = ""
    # validate column names
    expected_columns = ["date", "description", "category", "code", "income", "expense"]
    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        error_msg += f"Missing columns: {', '.join(missing_cols)}\n"

    df["income"] = (
        df["income"]
        .apply(
            lambda x: (float(x.replace(",", "")) if x else 0)
            if isinstance(x, str)
            else x
        )
        .apply(lambda x: round(x, 2) if not pd.isnull(x) else 0)
    )
    df["expense"] = (
        df["expense"]
        .apply(
            lambda x: (float(x.replace(",", "")) if x else 0)
            if isinstance(x, str)
            else x
        )
        .apply(lambda x: round(x, 2) if not pd.isnull(x) else 0)
    )
    # validate income/expense: No negative income/expense
    invalid_amounts = df[(df["income"] < 0) | (df["expense"] < 0)]
    if not invalid_amounts.empty:
        row_numbers = [index + 1 for index in invalid_amounts.index.tolist()]
        error_msg += f"Income or expense is negative in rows {row_numbers}\n"

    # Validate no row has both income and expense
    invalid_amounts = df[(df["income"] > 0) & (df["expense"] > 0)]
    if not invalid_amounts.empty:
        row_numbers = [index + 1 for index in invalid_amounts.index.tolist()]
        error_msg += f"rows {row_numbers} have both income and expense\n"
    try:
        df["date"] = pd.to_datetime(df["date"], format="mixed", dayfirst=False).dt.date
    except Exception as e:
        print(e)
        error_msg += f"Invalid date format: {e}\n"
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
                return

            df["inferred_category"] = False
            income_df = df[df["income"] > 0]
            expense_df = df[df["expense"] > 0]
            income_categories = [c.category for c in categories.filter(income=True)]
            expense_categories = [c.category for c in categories.filter(income=False)]
            default_income_category = categories.get(income=True, is_default=True).category
            default_expense_category = categories.get(income=False, is_default=True).category

            # infer categories
            income_df = infer_categories(
                income_df, income_categories, default_income_category, instance.user
            )
            expense_df = infer_categories(
                expense_df, expense_categories, default_expense_category, instance.user
            )
            # combine dataframes
            df = pd.concat([income_df, expense_df])

            with db_transaction.atomic():
                for index, row in df.iterrows():
                    category = categories.get(category=row["category"])
                    amount = row["income"] if row["income"] else row["expense"]
                    Transaction.objects.create(
                        date=row["date"],
                        description=row["description"],
                        amount=amount,
                        category=category,
                        code=row["code"],
                        file=instance,
                        inferred_category=row["inferred_category"],
                        user=instance.user,
                    )
                instance.status = Status.COMPLETED
                instance.save()
                return True
    except Exception as e:
        # print stacktrace
        import traceback

        traceback.print_exc()

        instance.status = Status.FAILED
        instance.message = str(e)
        instance.save()
        return False
