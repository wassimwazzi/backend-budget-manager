"""
Budget models
"""
from category.models import Category
from currency.models import Currency
from django.db import models
from django.db import connection
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
        super().save(*args, **kwargs)

    @staticmethod
    def get_budget_by_category(month, user):
        """
        Get the budget for each category for the given month.
        """
        start_date = month.replace(day=1)
        end_date = (
            month.replace(day=1) + relativedelta(months=1) - relativedelta(days=1)
        )
        user_id = user.id
        with connection.cursor() as cursor:
            cursor.execute(
                """
                WITH BUDGETSINCEDATE AS (
                    SELECT c.id AS category_id, c.CATEGORY, COALESCE(b.amount, 0) AS AMOUNT
                    FROM category_category c
                    LEFT OUTER JOIN budget_budget b ON b.category_id = c.id
                    WHERE c.INCOME = 0 AND (
                        b.start_date IS NULL
                        OR b.start_date = (
                            SELECT MAX(b2.start_date)
                            FROM budget_budget b2
                            WHERE b2.start_date <= %s
                            AND b2.category_id = c.id
                        )
                    ) AND c.user_id = %s
                ),

                TRANSACTIONSBUDGET AS (
                    SELECT b.CATEGORY AS Category, b.AMOUNT AS Budget,
                        COALESCE(SUM(t.amount),0) AS Actual, b.AMOUNT - COALESCE(SUM(t.amount),0) AS Remaining
                    FROM BUDGETSINCEDATE b
                    LEFT OUTER JOIN transaction_transaction t ON (
                        t.category_id = b.category_id AND
                        t.date >= %s AND
                        t.date <= %s
                    )
                    GROUP BY b.CATEGORY
                    ORDER BY Remaining ASC
                )

                SELECT Category, Budget, ROUND(Actual, 2) AS Actual, ROUND(Remaining, 2) AS Remaining
                FROM TRANSACTIONSBUDGET
                WHERE Actual > 0 OR budget > 0
                ;
            """,
                [start_date, user_id, start_date, end_date],
            )
            budget_summary_query = cursor.fetchall()
            budget_summary = [
                {
                    "category": budget[0],
                    "budget": budget[1],
                    "actual": budget[2],
                    "remaining": budget[3],
                }
                for budget in budget_summary_query
            ]
        return budget_summary
