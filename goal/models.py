"""
Goal Model
"""
from django.db import models
from django.contrib.auth.models import User
import calendar


class GoalType(models.TextChoices):
    """
    Goal Type
    """

    SAVINGS = "SAVINGS"
    DEBT = "DEBT"
    INVESTMENT = "INVESTMENT"


class GoalStatus(models.TextChoices):
    """
    Goal Status
    """

    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Goal(models.Model):
    """
    Goal Model
    """

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expected_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=GoalType.choices)
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=GoalStatus.choices, default=GoalStatus.IN_PROGRESS
    )
    start_date = models.DateField(auto_now_add=True)
    recurring = models.BooleanField(default=False)
    reccuring_frequency = models.PositiveIntegerField(null=True, blank=True) # in months
    previous_goal = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} - {self.type}"

    class Meta:
        """
        Meta class for Currency
        """

        verbose_name_plural = "goals"

class GoalContribution(models.Model):
    """
    Goal Contribution Model
    A job runs at the start of each month to create a contribution for each goal, and calculate the amount
    """

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # calculated automatically at the end of the month
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True) # auto set to the end of the month
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} - {self.date}"
    
    def save(self, *args, **kwargs):
        """
        - Set start date to the first of the month
        - Set end date to the last day of the month
        """
        self.start_date = self.start_date.replace(day=1)
        end_of_month = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
        self.end_date = self.start_date.replace(day=end_of_month)
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for Currency
        """

        verbose_name_plural = "goal contributions"