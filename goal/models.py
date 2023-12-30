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
import logging


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


def find_gaps(ranges, start, end, interval=datetime.timedelta(days=1)):
    """
    Finds all the gaps in the given ranges, between start and end.
    """
    # Sort the array based on the start dates
    sorted_ranges = sorted(ranges)
    result = []

    for range in sorted_ranges:
        if range[0] > start:
            result.append((start, range[0] - interval))
        start = range[1] + interval

    if end > start - interval:
        result.append((start, end))

    return result


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
            ContributionRange.get_overlapping_ranges(
                self.user, self.start_date, self.end_date
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "Cannot have overlapping contribution ranges."
            )
        super().save(*args, **kwargs)

    @staticmethod
    def get_overlapping_ranges(user, start_date, end_date):
        """
        Get all contribution ranges that overlap with the given range
        """
        return ContributionRange.objects.filter(user=user).filter(
            models.Q(start_date__lte=start_date, end_date__gte=start_date)
            | models.Q(start_date__lte=end_date, end_date__gte=end_date)
            | models.Q(start_date__gte=start_date, end_date__lte=end_date)
        )

    @staticmethod
    def _handle_case_1(overlapping_range, start_date, end_date, contributions):
        """
        Case 1: overlapping_range.start_date <= start_date <= end_date <= overlapping_range.end_date
        new range is a subinterval of the existing range
        split old range into 2 new ranges, and create new range from start_date to end_date
          part 1: overlapping_range.start_date to start_date, and copy over the contributions
          part 2: end_date to overlapping_range.end_date and copy over the contributions
          Create new range: start_date to end_date, and add the contributions of old range to it
        """
        logging.info("Case 1: %s, %s, %s", overlapping_range, start_date, end_date)
        user = overlapping_range.user
        result = []
        # split into 2.
        # 1. overlapping_range.start_date to start_date
        # 2. start_date to end_date
        overlapping_range_end_date = overlapping_range.end_date
        overlapping_range.end_date = start_date - datetime.timedelta(days=1)
        overlapping_range.save()  # all contributions are kept
        logging.info(
            "set end date of old range %s to %s", overlapping_range, start_date
        )
        result.append(overlapping_range)
        # create new range for the end_date to overlapping_range.end_date
        old_range_right_side = ContributionRange.objects.create(
            user=user,
            start_date=end_date + datetime.timedelta(days=1),
            end_date=overlapping_range_end_date,
        )
        logging.info(
            "created new range for old right hand side %s from %s to %s",
            old_range_right_side,
            end_date + datetime.timedelta(days=1),
            overlapping_range_end_date,
        )
        # create new range for start_date to end_date
        new_range = ContributionRange.objects.create(
            user=user, start_date=start_date, end_date=end_date
        )
        logging.info(
            "created new range %s from %s to %s",
            new_range,
            start_date,
            end_date,
        )
        # flip order so they are sorted by start_date
        result.append(new_range)
        result.append(old_range_right_side)
        # add contributions to new range
        # add contributions back to old range (right side)
        for contribution in contributions:
            GoalContribution.objects.create(
                goal=contribution.goal,
                percentage=contribution.percentage,
                date_range=old_range_right_side,
            )
            GoalContribution.objects.create(
                goal=contribution.goal,
                percentage=contribution.percentage,
                date_range=new_range,
            )
        return result

    @staticmethod
    def _handle_case_2(overlapping_range, start_date, end_date, contributions):
        """
        Case 2: start_date <= overlapping_range.start_date <= end_date <= overlapping_range.end_date
        shift old range to the right: overlapping_range.start_date = end_date + 1, keep same contributions
        create new range from overlapping_range.start_date to end_date, and add the contributions of old range to it
        add this new range to result
        """
        logging.info("Case 2: %s, %s, %s", overlapping_range, start_date, end_date)
        result = []
        # shift old range to the right
        overlapping_range_start_date = overlapping_range.start_date
        overlapping_range.start_date = end_date + datetime.timedelta(days=1)
        overlapping_range.save()
        logging.info(
            "set start date of old range from %s to %s",
            overlapping_range_start_date,
            overlapping_range.start_date,
        )
        # create new range from overlapping_range.start_date to end_date
        new_range = ContributionRange.objects.create(
            user=overlapping_range.user,
            start_date=overlapping_range_start_date,
            end_date=end_date,
        )
        result.append(new_range)
        result.append(overlapping_range)  # flip order so they are sorted by start_date
        logging.info(
            "created new range %s from %s to %s",
            new_range,
            overlapping_range_start_date,
            end_date,
        )
        # add contributions to new range
        for contribution in contributions:
            GoalContribution.objects.create(
                goal=contribution.goal,
                percentage=contribution.percentage,
                date_range=new_range,
            )
        return result

    @staticmethod
    def _handle_case_3(overlapping_range, start_date, end_date, contributions):
        """
        Case 3: overlapping_range.start_date <= start_date <= overlapping_range.end_date <= end_date
        shift old range to the left: overlapping_range.end_date = start_date - 1, keep same contributions
        create new range from start_date to overlapping_range.end_date, and add the contributions of old range to it
        add this new range to result
        """
        logging.info("Case 3: %s, %s, %s", overlapping_range, start_date, end_date)
        result = []
        # shift old range to the left
        overlapping_range_end_date = overlapping_range.end_date
        overlapping_range.end_date = start_date - datetime.timedelta(days=1)
        overlapping_range.save()
        logging.info(
            "set end date of old range from %s to %s",
            overlapping_range_end_date,
            overlapping_range.end_date,
        )
        # create new range from start_date to overlapping_range.end_date
        new_range = ContributionRange.objects.create(
            user=overlapping_range.user,
            start_date=start_date,
            end_date=overlapping_range_end_date,
        )
        result.append(overlapping_range)
        result.append(new_range)
        logging.info(
            "created new range %s from %s to %s",
            new_range,
            start_date,
            overlapping_range_end_date,
        )
        # add contributions to new range
        for contribution in contributions:
            GoalContribution.objects.create(
                goal=contribution.goal,
                percentage=contribution.percentage,
                date_range=new_range,
            )
        return result

    @staticmethod
    def _handle_case_4(overlapping_range, start_date, end_date, _contributions):
        """
        Case 4: start_date <= overlapping_range.start_date <= overlapping_range.end_date <= end_date
        overlapping_range is a subinterval of the new range
        keep old range, and add it to result
        """
        logging.info("Case 4: %s, %s, %s", overlapping_range, start_date, end_date)
        logging.info("keep old range %s", overlapping_range)
        return [overlapping_range]

    @staticmethod
    def add_new_range(user, start_date, end_date):
        """
        Create a new contribution range for a user.
        If range already exists, do nothing.
        If start and end date are within an existing range, split the existing range into 2 or 3 based on the dates.
        If start and end date are outside of an existing range, create a new range.
        Re-assign all goal contributions to the new ranges. Create new goal contributions if necessary.
        """
        logging.info(
            "Adding new range for %s from %s to %s", user, start_date, end_date
        )
        overlapping_ranges = ContributionRange.get_overlapping_ranges(
            user, start_date, end_date
        )
        if not overlapping_ranges.exists():
            logging.info("No overlapping ranges found. Creating new range with full dates.")
            new_range = ContributionRange.objects.create(
                user=user, start_date=start_date, end_date=end_date
            )
            return [new_range]

        logging.info("Found overlapping ranges: %s", overlapping_ranges)

        filled_ranges = []
        result = []
        # NOTE: The overlapping ranges cannot overlap with each other, by db integrity
        for overlapping_range in overlapping_ranges:
            # 4 cases:
            # 1. overlapping_range.start_date <= start_date <= end_date <= overlapping_range.end_date
            #    new range is a subinterval of the existing range
            #    split old range into 2 new ranges, and create new range from start_date to end_date
            #      part 1: overlapping_range.start_date to start_date, and copy over the contributions
            #      part 2: end_date to overlapping_range.end_date and copy over the contributions
            #      Create new range: start_date to end_date, and add the contributions of old range to it
            #    This case also means that there's only 1 overlapping range
            # 2. start_date <= overlapping_range.start_date <= end_date <= overlapping_range.end_date
            #    shift old range to the right: overlapping_range.start_date = end_date + 1, keep same contributions
            #    create new range from overlapping_range.start_date to end_date, and add the contributions of old range to it
            #    add this new range to result
            # 3. overlapping_range.start_date <= start_date <= overlapping_range.end_date <= end_date
            #    shift old range to the left: overlapping_range.end_date = start_date - 1, keep same contributions
            #    create new range from start_date to overlapping_range.end_date, and add the contributions of old range to it
            #    add this new range to result
            # 4. start_date <= overlapping_range.start_date <= overlapping_range.end_date <= end_date
            #    overlapping_range is a subinterval of the new range
            #    keep old range, and add it to result
            # ##
            # At the end, we need to fill in the gaps, if any.
            # Example, if case 4 is the only overlapping range, then we need to create 2 new ranges:
            # 1. start_date to overlapping_range.start_date - 1
            # 2. overlapping_range.end_date + 1 to end_date

            contributions = overlapping_range.contributions.all()
            # Case 1
            if (
                overlapping_range.start_date <= start_date
                and end_date <= overlapping_range.end_date
            ):
                # no gap to fill
                # we can return here, since we know there's only 1 overlapping range
                return ContributionRange._handle_case_1(
                    overlapping_range, start_date, end_date, contributions
                )
            # Case 2
            if (
                start_date <= overlapping_range.start_date
                and end_date <= overlapping_range.end_date
            ):
                new_ranges = ContributionRange._handle_case_2(
                    overlapping_range, start_date, end_date, contributions
                )
                result += new_ranges
                new_range = new_ranges[0]
                # add to filled_ranges
                filled_ranges.append((new_range.start_date, new_range.end_date))
                continue
            # Case 3
            if (
                overlapping_range.start_date <= start_date
                and overlapping_range.end_date <= end_date
            ):
                new_ranges = ContributionRange._handle_case_3(
                    overlapping_range, start_date, end_date, contributions
                )
                result += new_ranges
                new_range = new_ranges[1]
                # add to filled_ranges
                filled_ranges.append((new_range.start_date, new_range.end_date))
                continue
            # Case 4
            if (
                start_date <= overlapping_range.start_date
                and overlapping_range.end_date <= end_date
            ):
                new_range = ContributionRange._handle_case_4(
                    overlapping_range, start_date, end_date, contributions
                )[0]
                result.append(new_range)
                # add to filled_ranges
                filled_ranges.append((new_range.start_date, new_range.end_date))
                continue

        gaps = find_gaps(filled_ranges, start_date, end_date)
        logging.info("Found gaps: %s", gaps)
        for gap in gaps:
            new_range = ContributionRange.objects.create(
                user=user, start_date=gap[0], end_date=gap[1]
            )
            result.append(new_range)

        result = sorted(result, key=lambda x: x.start_date)
        logging.info("Add new range result: %s", result)
        return result

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
