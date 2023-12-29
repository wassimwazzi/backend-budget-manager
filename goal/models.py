"""
Goal Model
"""
from django.db import models
from django.contrib.auth.models import User
import django.core.exceptions
import calendar
import datetime


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

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class GoalRecurranceType(models.TextChoices):
    """
    Goal Recurrance Type
    """

    INDEFINITE = "INDEFINITE"
    FIXED = "FIXED"
    NON_RECURRING = "NON_RECURRING"


class Goal(models.Model):
    """
    Goal Model
    """

    id = models.AutoField(primary_key=True)
    amount = models.PositiveIntegerField()
    expected_completion_date = models.DateField()  # YYYY-MM
    actual_completion_date = models.DateField(null=True, blank=True)
    type = models.CharField(
        max_length=20, choices=GoalType.choices, default=GoalType.SAVINGS
    )
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=GoalStatus.choices, default=GoalStatus.IN_PROGRESS
    )
    start_date = models.DateField()
    recurring = models.CharField(
        max_length=20,
        choices=GoalRecurranceType.choices,
        default=GoalRecurranceType.NON_RECURRING,
    )
    reccuring_frequency = models.PositiveIntegerField(
        null=True, blank=True
    )  # in months
    previous_goal = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} - {self.type}"

    def validate_completion_date(self):
        if self.expected_completion_date < datetime.date.today():
            raise django.core.exceptions.ValidationError(
                "Completion date must be in the future."
            )
        if self.expected_completion_date < self.start_date:
            raise django.core.exceptions.ValidationError(
                "Completion date must be after start date."
            )
        end_completion_date = calendar.monthrange(
            self.expected_completion_date.year, self.expected_completion_date.month
        )[1]
        self.expected_completion_date = self.expected_completion_date.replace(
            day=end_completion_date
        )

    def validate_actual_completion_date(self):
        if not self.actual_completion_date:
            return
        if self.actual_completion_date < self.start_date:
            raise django.core.exceptions.ValidationError(
                "Actual completion date must be after start date."
            )

    def validate_recurring(self):
        """
        Check that recurring goals have a frequency
        """
        if self.recurring != GoalRecurranceType.NON_RECURRING and not self.reccuring_frequency:
            raise django.core.exceptions.ValidationError(
                "Recurring goals must have a frequency."
            )

    def validate_status(self):
        if self.status == GoalStatus.COMPLETED and not self.actual_completion_date:
            self.actual_completion_date = datetime.date.today()
        if self.status != GoalStatus.COMPLETED and self.actual_completion_date:
            raise django.core.exceptions.ValidationError(
                "Actual completion date cannot be set if goal is not completed."
            )

    def save(self, *args, **kwargs):
        """
        - Set start date to today if not given
        - Check that completion date is after start date
        """
        self.validate_recurring()
        if not self.start_date:
            self.start_date = datetime.date.today()
        self.start_date = self.start_date.replace(day=1)
        self.validate_completion_date()
        self.validate_actual_completion_date()
        self.validate_status()
        self.full_clean()  # validate model
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for goal
        """

        verbose_name_plural = "goals"


class GoalContribution(models.Model):
    """
    Goal Contribution Model
    A job runs at the start of each month to create a contribution for each goal, and calculate the amount
    """

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # calculated automatically at the end of the month
    start_date = models.DateField()
    end_date = models.DateField(
        null=True, blank=True
    )  # auto set to the end of the month
    percentage = models.IntegerField(
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(100),
        ]
    )
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.goal}: {self.amount} - {self.start_date}"

    def validate_percentage(self):
        """
        The percentages of ALL user contributions for a given month cannot sum to more than 100
        """
        total_existing_percentage = (
            GoalContribution.objects.filter(
                start_date=self.start_date, goal__user=self.goal.user
            ).aggregate(models.Sum("percentage"))["percentage__sum"]
            or 0
        )
        if total_existing_percentage + self.percentage > 100:
            raise django.core.exceptions.ValidationError(
                "Percentages cannot sum to more than 100."
            )

    def save(self, *args, **kwargs):
        """
        - Set start date to the first of the month
        - Set end date to the last day of the month
        """
        if not self.pk:  # if creating a new contribution
            # Cannot create a contribution for a completed goal
            if self.goal.status == GoalStatus.COMPLETED:
                raise django.core.exceptions.ValidationError(
                    "Cannot create a contribution for a completed goal."
                )
        self.full_clean()  # validate model
        if not self.start_date:
            self.start_date = datetime.date.today()
        self.start_date = self.start_date.replace(day=1)
        if self.start_date < self.goal.start_date:
            raise django.core.exceptions.ValidationError(
                "Contribution start date cannot be before goal start date."
            )
        end_of_month = calendar.monthrange(self.start_date.year, self.start_date.month)[
            1
        ]
        self.end_date = self.start_date.replace(day=end_of_month)
        self.validate_percentage()  # call after setting end_date and start_date
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for goal contribution
        """

        verbose_name_plural = "goal contributions"
        constraints = [
            models.UniqueConstraint(
                fields=["goal", "start_date"], name="unique_goal_contribution"
            ),
        ]
