"""
Budget models
"""
from category.models import Category
from currency.models import Currency
from transaction.models import Transaction
from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta


class Budget(models.Model):
    """
    A budget for a category for a month, beginning from start_date.
    Each subsequest month will use the same budget until a new budget with a new start_date is created.
    Can only have one budget per category per period of time.
    """

    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    start_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "start_date", "user"], name="unique_budget"
            ),
        ]

    def __str__(self):
        return f"{self.category} - {self.start_date}: {self.amount} {self.currency}"

    def save(self, *args, **kwargs):
        """
        Set date to first day of month.
        """
        self.start_date = self.start_date.replace(day=1)
        if self.amount < 0:
            raise IntegrityError("Budget amount must be positive.")
        if self.category.user != self.user:
            raise IntegrityError("Category must belong to user.")
        super().save(*args, **kwargs)

    @staticmethod
    def get_budget_by_category(month, user):
        """
        Like get_budget_by_category but using Django ORM.
        """
        start_date = month.replace(day=1)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        # For each category, get the most recent budget before the start date
        # If no budget exists for the month and category, but a transaction exists, set budget to 0
        budgets = (
            Budget.objects.filter(
                start_date__lte=start_date,
                category__income=False,
                user=user,
                start_date=models.Subquery(
                    Budget.objects.filter(
                        category=models.OuterRef("category"), start_date__lte=start_date
                    )
                    .values("category__category")
                    .annotate(max_start_date=models.Max("start_date"))
                    .values("max_start_date")[:1]
                ),
            )
            .annotate(budget=models.F("amount"))
            .values("category__category", "budget", "start_date")
        )
        # For each category, get the sum of transactions for the month
        # If no transaction exists for the month and category, but a budget exists, set actual to 0
        transactions = (
            Transaction.objects.filter(
                category__income=False,
                date__gte=start_date,
                date__lte=end_date,
                user=user,
            )
            .values(
                "category__category",
            )
            .annotate(
                actual=models.Sum("amount"),
            )
            .values(
                "category__category",
                "actual",
            )
        )
        # Combine budgets and transactions
        # get set of categories
        categories = set(budget["category__category"] for budget in budgets).union(
            set(transaction["category__category"] for transaction in transactions)
        )
        budget_summary = []
        for category in categories:
            budget = next(
                (
                    budget
                    for budget in budgets
                    if budget["category__category"] == category
                ),
                {"budget": 0},
            )
            transaction = next(
                (
                    transaction
                    for transaction in transactions
                    if transaction["category__category"] == category
                ),
                {"actual": 0},
            )
            budget_summary.append(
                {
                    "category": category,
                    "budget": budget["budget"],
                    "actual": transaction["actual"],
                    "remaining": budget["budget"] - transaction["actual"],
                }
            )
        return budget_summary
