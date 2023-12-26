from huey.contrib.djhuey import db_task
from transaction.models import Transaction
from django.contrib.auth.models import User
from inference.inference import infer_categories


@db_task()
def infer_categories_task(user_id, webhook_url=None):
    user = User.objects.get(id=user_id)
    transactions = Transaction.objects.filter(user=user, inferred_category=True)
    infer_categories(transactions, user)
    return True
