"""
Goal Model
"""
from django.db import models
from django.contrib.auth.models import User
import django.core.exceptions
from transaction.models import Transaction
import decimal
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
        if (
            self.recurring != GoalRecurranceType.NON_RECURRING
            and not self.reccuring_frequency
        ):
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

    def get_progress(self, percentage=False):
        """
        Calculate the progress of the goal.
        For each contribution, calculate the amount contributed to the goal.
        Then, sum all the contributions.
        """
        contributions = GoalContribution.objects.filter(goal=self)
        total_contribution = sum(c.contribution for c in contributions)
        if percentage:
            return total_contribution / self.amount * 100
        return total_contribution

    class Meta:
        """
        Meta class for goal
        """

        verbose_name_plural = "goals"


class ContributionRange(models.Model):
    """
    Contribution Range Model
    """

    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.start_date} - {self.end_date}"

    def save(self, *args, **kwargs):
        """
        Ranges are unique over the entire period for a user
        """
        if (
            ContributionRange.objects.filter(user=self.user)
            .filter(
                models.Q(start_date__lte=self.start_date, end_date__gte=self.start_date)
                | models.Q(start_date__lte=self.end_date, end_date__gte=self.end_date)
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "Cannot have overlapping contribution ranges."
            )
        super().save(*args, **kwargs)

    class Meta:
        """
        Meta class for contribution range
        """

        verbose_name_plural = "contribution ranges"


class GoalContribution(models.Model):
    """
    Goal Contribution Model
    A job runs at the start of each month to create a contribution for each goal, and calculate the amount
    """

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Cache result at the end of the month
    percentage = models.PositiveIntegerField(
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(100),
        ]
    )
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name="contributions"
    )
    date_range = models.ForeignKey(
        ContributionRange, on_delete=models.PROTECT, related_name="contributions"
    )

    def __str__(self):
        return f"{self.goal}: {self.amount} - {self.start_date}"

    def validate_percentage(self):
        """
        The percentages of ALL user contributions for a given month cannot sum to more than 100
        """
        total_existing_percentage = (
            ContributionRange.objects.get(
                id=self.date_range.id
            ).contributions.aggregate(models.Sum("percentage"))["percentage__sum"]
            or 0
        )
        if total_existing_percentage + self.percentage > 100:
            raise django.core.exceptions.ValidationError(
                "Percentages cannot sum to more than 100."
            )

    def validate_range(self):
        """
        The contribution range must be in the same month as the goal
        """
        if self.date_range.start_date < self.goal.start_date:
            raise django.core.exceptions.ValidationError(
                "Contribution range cannot be before goal start date."
            )
        if self.date_range.end_date > self.goal.expected_completion_date:
            raise django.core.exceptions.ValidationError(
                "Contribution range cannot be after goal completion date."
            )

    def save(self, *args, **kwargs):
        if not self.pk:  # if creating a new contribution
            if self.goal.status == GoalStatus.COMPLETED:
                raise django.core.exceptions.ValidationError(
                    "Cannot create a contribution for a completed goal."
                )
        self.validate_range()
        self.validate_percentage()
        super().save(*args, **kwargs)

    @property
    def contribution(self):
        """
        Calculate how much was contributed to the goal for this contribution
        """
        if self.amount:
            return self.amount
        start_date = self.date_range.start_date
        end_date = self.date_range.end_date
        transactions_by_type = (
            Transaction.objects.filter(
                user=self.goal.user,
                date__gte=start_date,
                date__lte=end_date,
            )
            .values("category__income")
            .annotate(total=models.Sum("amount"))
        )  # returns 2 rows, one for income and one for expenses
        net_saved = 0
        for i in transactions_by_type:
            if i["category__income"]:
                net_saved += i["total"]
            else:
                net_saved -= i["total"]
        return net_saved * decimal.Decimal(self.percentage / 100)

    class Meta:
        """
        Meta class for goal contribution
        """

        verbose_name_plural = "goal contributions"
