import logging
from thefuzz import fuzz
from text_classifier import SimpleClassifier, fuzzy_search
from category.models import Category
from transaction.models import Transaction
from django.db import transaction as db_transaction


text_classifier = SimpleClassifier()


def _infer(transactions_to_infer, categories, default_category):
    # infers for either income or expense.
    category_names = [c.category for c in categories]
    user = default_category.user
    prev_inferred_transactions = Transaction.objects.filter(
        inferred_category=True, user=user
    ).exclude(category=default_category)
    prev_non_inferred_transactions = Transaction.objects.filter(
        inferred_category=False, user=user
    )
    prev_inferred_codes = {
        t.code: t.category for t in prev_inferred_transactions if t.code
    }
    prev_inferred_descriptions = {
        t.description: t.category for t in prev_inferred_transactions if t.description
    }
    prev_non_inferred_codes = {
        t.code: t.category for t in prev_non_inferred_transactions if t.code
    }
    prev_non_inferred_descriptions = {
        t.description: t.category
        for t in prev_non_inferred_transactions
        if t.description
    }
    for transaction in transactions_to_infer:
        logging.debug("Infering category for\n %s", transaction)
        code = transaction.code
        description = transaction.description
        if not code and not description:
            logging.debug(
                "Using default category as no description or code. %s", transaction
            )
            transaction.category = default_category
            transaction.inferred_category = True
            transaction.save()
            continue

        if code:
            # Prioritise non-inferred transactions
            logging.debug(
                "Searching for previous non inferred transactions with code %s", code
            )
            prev_code = fuzzy_search(
                code, prev_non_inferred_codes.keys(), scorer=fuzz.token_set_ratio
            )
            if prev_code:
                prev_category = prev_non_inferred_codes[prev_code]
                logging.debug(
                    """Found previous non inferred transaction %s with similar code to %s.
                    Using previous category: %s""",
                    prev_code,
                    code,
                    prev_category,
                )
                transaction.category = prev_category
                transaction.inferred_category = True
                transaction.save()
                continue
            # if previous transaction has same code, use that category
            logging.debug(
                "Searching for previous inferred transactions with code %s", code
            )
            prev_code = fuzzy_search(
                code, prev_inferred_codes.keys(), scorer=fuzz.token_set_ratio
            )
            if prev_code:
                prev_category = prev_inferred_codes[prev_code]
                logging.debug(
                    """Found previous inferred transaction %s with similar code to %s.
                    Using previous category: %s""",
                    prev_code,
                    code,
                    prev_category,
                )
                transaction.category = prev_category
                transaction.inferred_category = True
                transaction.save()
                continue

        if description:
            # Prioritise non-inferred transactions
            logging.debug(
                "Searching for previous non inferred transactions with description %s",
                description,
            )
            prev_description = fuzzy_search(
                description,
                prev_non_inferred_descriptions.keys(),
                scorer=fuzz.token_sort_ratio,
            )
            if prev_description:
                prev_category = prev_non_inferred_descriptions[prev_description]
                logging.debug(
                    """Found previous non inferred transaction %s with similar description to %s.
                    Using previous category: %s""",
                    prev_description,
                    description,
                    prev_category,
                )
                transaction.category = prev_category
                transaction.inferred_category = True
                transaction.save()
                continue
            logging.debug(
                "Searching for previous inferred transactions with description %s",
                description,
            )
            prev_description = fuzzy_search(
                description,
                prev_inferred_descriptions.keys(),
                scorer=fuzz.token_sort_ratio,
            )
            if prev_description:
                prev_category = prev_inferred_descriptions[prev_description]
                logging.debug(
                    """Found previous inferred transaction %s with similar description to %s.
                    Using previous category: %s""",
                    prev_description,
                    description,
                    prev_category,
                )
                transaction.category = prev_category
                transaction.inferred_category = True
                transaction.save()
                continue

            # if no previous transaction has same description, use NLP
            # Only use NLP on description as we will rarely get a match on code
            result = text_classifier.predict(description, category_names)
            if result:
                logging.debug(
                    "Inferred category using NLP for %s: %s", description, result
                )
                transaction.category = categories.get(category=result)
                transaction.inferred_category = True
                transaction.save()
                # add to previous transactions
                prev_inferred_descriptions[description] = result
                if code:
                    prev_inferred_codes[code] = result
                continue
        logging.debug(
            "Using default category as no description was given and couldn't match code. %s",
            transaction,
        )


def infer_categories(transactions, user):
    """
    Auto fill the category column when missing.
    If the category is already in the db, use that
    If the code is the same as a previous transaction (fuzzy search), use that category
    Otherwise, use NLP to infer category
    """
    income_transactions = transactions.filter(category__income=True)
    expense_transactions = transactions.filter(category__income=False)
    income_categories = Category.objects.filter(user=user, income=True)
    expense_categories = Category.objects.filter(user=user, income=False)
    default_income_category = income_categories.get(is_default=True)
    default_expense_category = expense_categories.get(is_default=True)
    with db_transaction.atomic():
        _infer(income_transactions, income_categories, default_income_category)
        _infer(expense_transactions, expense_categories, default_expense_category)
