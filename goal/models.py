"""
Goal Model
"""
from django.db import models, transaction
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
        end_completion_date = calendar.monthrange(
            self.expected_completion_date.year, self.expected_completion_date.month
        )[1]
        self.expected_completion_date = self.expected_completion_date.replace(
            day=end_completion_date
        )
        if self.expected_completion_date < datetime.date.today():
            raise django.core.exceptions.ValidationError(
                "Completion date must be in the future."
            )
        if self.expected_completion_date < self.start_date:
            raise django.core.exceptions.ValidationError(
                "Completion date must be after start date."
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

    def finalize(self, redistribute_percentages=False):
        """
        Finalize the goal.
        - Set actual completion date to today
        - Set status to completed
        - Sets the amount on all contributions
        """
        with transaction.atomic():
            total = 0
            for contribution in self.contributions.all().order_by(
                "date_range__start_date"
            ):
                amount = contribution.finalize(self.amount - total)
                total += amount

            if total < self.amount:
                self.status = GoalStatus.FAILED
            else:
                self.actual_completion_date = datetime.date.today()
                self.status = GoalStatus.COMPLETED
            self.save()
            if redistribute_percentages:
                for contribution_range in self.contribution_ranges:
                    contribution_range.distribute_remaining_percentages()

    @property
    def is_finalized(self):
        """
        Check if goal is finalized
        """
        return self.status in [GoalStatus.COMPLETED, GoalStatus.FAILED]

    @property
    def progress(self):
        return self.total_contributed / self.amount * 100

    @property
    def total_contributed(self):
        """
        Calculate the total amount contributed to the goal.
        """
        total_contribution = sum(c.contribution for c in self.contributions.all())
        return min(total_contribution, self.amount)

    @property
    def contribution_ranges(self):
        """
        Get all contribution ranges for this goal.
        """
        return ContributionRange.objects.filter(
            id__in=self.contributions.values_list("date_range__id", flat=True)
        )

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
    Contribution Range Model.
    WARN: Only create ranges with start date at beginning of month, and end date at end of month.
    This is not enforced by the model, but it should be guaranteed given how goals dates are.
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
        if self.start_date >= self.end_date:
            raise django.core.exceptions.ValidationError(
                "Start date must be before end date."
            )
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

    def update_contributions(self, contributions):
        """
        Update the contributions for this range.
        contributions is a list of dictionaries, with keys goal, percentage, and amount
        """
        with transaction.atomic():
            self.contributions.all().delete()
            for contribution in contributions:
                goal = Goal.objects.get(id=contribution["goal"]["id"])
                GoalContribution.objects.create(
                    goal=goal,
                    percentage=contribution["percentage"],
                    amount=contribution.get("amount"),
                    date_range=self,
                )

    def distribute_remaining_percentages(self):
        """
        If the total percentage of all contributions in this range is less than 100,
        distribute the remaining percentage to all contributions evenly, ensuring that total is 100, and percentages are integers
        If contribution's goal is finalized, do not update its percentage
        """
        total_percentage = self.total_percentage
        if total_percentage == 100:
            return
        remaining_percentage = 100 - total_percentage
        non_finalized_contributions = list(
            filter(lambda x: not x.goal.is_finalized, self.contributions.all())
        )
        num_contributions = len(non_finalized_contributions)
        if num_contributions == 0:
            return
        per_contribution_percentage = remaining_percentage // num_contributions
        remainder = remaining_percentage % num_contributions
        for contribution in non_finalized_contributions:
            percentage_to_add = per_contribution_percentage
            if remainder > 0:
                percentage_to_add += 1
                remainder -= 1
            contribution.percentage += percentage_to_add
            contribution.save()

    @property
    def total_percentage(self):
        """
        Calculate the total percentage of all contributions in this range
        """
        return (
            self.contributions.aggregate(models.Sum("percentage"))["percentage__sum"]
            or 0
        )

    @property
    def transactions_net_amount(self):
        """
        Calculate the net saved amount of transactions in this range
        """
        transactions = (
            Transaction.objects.filter(
                user=self.user,
                date__gte=self.start_date,
                date__lte=self.end_date,
            )
            .values("category__income")
            .annotate(total=models.Sum("amount"))
        )  # returns 2 rows, one for income and one for expenses
        net_saved = next(
            (i["total"] for i in transactions if i["category__income"] and i["total"]),
            0,
        )
        net_saved -= next(
            (
                i["total"]
                for i in transactions
                if not i["category__income"] and i["total"]
            ),
            0,
        )
        return net_saved

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
            logging.info(
                "No overlapping ranges found. Creating new range with full dates."
            )
            new_range = ContributionRange.objects.create(
                user=user, start_date=start_date, end_date=end_date
            )
            return [new_range]

        logging.info("Found overlapping ranges: %s", overlapping_ranges)

        filled_ranges = []
        result = []
        with transaction.atomic():
            # NOTE: The overlapping ranges cannot overlap with each other, by db integrity
            for overlapping_range in overlapping_ranges:
                # 4 cases:
                # 1. overlapping_range.start_date <= start_date <= end_date <= overlapping_range.end_date
                #    This case also means that there's only 1 overlapping range
                #    - 1.1 overlapping_range.start_date == start_date and overlapping_range.end_date == end_date
                #        no need to split range. No change.
                #    - 1.2 overlapping_range.start_date == start_date and end_date < overlapping_range.end_date
                #        Return 2 ranges from start_date to end_date, and from end_date + 1 to overlapping_range.end_date
                #        add the contributions of old range to both ranges
                #    - 1.3 overlapping_range.start_date < start_date and overlapping_range.end_date == end_date
                #        Return 2 ranges from overlapping_range.start_date to start_date - 1, and from start_date to end_date
                #        add the contributions of old range to both ranges
                #    - 1.4 overlapping_range.start_date < start_date and end_date < overlapping_range.end_date
                #        Return 3 ranges from overlapping_range.start_date to start_date - 1,
                #        from start_date to end_date, and from end_date + 1 to overlapping_range.end_date
                #        add the contributions of old range to all 3 ranges
                # 2. start_date < overlapping_range.start_date <= end_date <= overlapping_range.end_date
                #    NOTE: In theory, this case should never happen, since we should always be creating ranges from start of month to end of month
                #    - 2.1 overlapping_range.start_date < end_date and end_date == overlapping_range.end_date
                #        Returns 1 range, the overlapping range
                #    - 2.2 overlapping_range.start_date == end_date
                #        Returns 2 ranges
                #        shift old range to the right: overlapping_range.start_date = end_date + 1, keep same contributions
                #        create new range from overlapping_range.start_date to end_date, and add the contributions of old range to it
                #    - 2.3 overlapping_range.start_date < end_date < overlapping_range.end_date
                #        Returns 2 ranges
                #        shift old range to the right: overlapping_range.start_date = end_date + 1, keep same contributions
                #        create new range from overlapping_range.start_date to end_date, and add the contributions of old range to it
                #        add this new range to result
                # 3. overlapping_range.start_date <= start_date <= overlapping_range.end_date < end_date
                #    - 3.1 overlapping_range.start_date == start_date
                #        Returns 2 ranges
                #
                #    shift old range to the left: overlapping_range.end_date = start_date - 1, keep same contributions
                #    create new range from start_date to overlapping_range.end_date, and add the contributions of old range to it
                #    add this new range to result
                # 4. start_date < overlapping_range.start_date < overlapping_range.end_date < end_date
                #    overlapping_range is a subinterval of the new range
                #    keep old range, and add it to result
                # ##
                # At the end, we need to fill in the gaps, if any.
                # Example, if case 4 is the only overlapping range, then we need to create 2 new ranges:
                # 1. start_date to overlapping_range.start_date - 1
                # 2. overlapping_range.end_date + 1 to end_date

                contributions = overlapping_range.contributions.all()

                def add_contributions(contributions, date_range):
                    for contribution in contributions:
                        GoalContribution.objects.create(
                            goal=contribution["goal"],
                            percentage=contribution["percentage"],
                            date_range=date_range,
                        )

                contributions_backup = list(
                    map(
                        lambda x: {"goal": x.goal, "percentage": x.percentage},
                        contributions,
                    )
                )
                # delete all contributions from old range
                contributions.delete()
                contributions = contributions_backup
                # delete the old range
                overlapping_range_start_date = overlapping_range.start_date
                overlapping_range_end_date = overlapping_range.end_date
                user = overlapping_range.user
                overlapping_range.delete()

                new_start_to_overlapping_start = (
                    overlapping_range_start_date - start_date
                )  # IGNORE
                overlapping_start_to_new_start = (
                    start_date - overlapping_range_start_date
                )
                new_start_to_overlapping_end = overlapping_range_end_date - start_date
                new_start_to_new_end = end_date - start_date
                new_end_to_overlapping_end = overlapping_range_end_date - end_date
                overlapping_end_to_new_end = (
                    end_date - overlapping_range_end_date
                )  # IGNORE
                # never create from start date to overlapping range start date, these will be the gaps.
                # left side
                ranges = []
                logging.debug(
                    "new_start_to_overlapping_start: %s", new_start_to_overlapping_start
                )
                logging.debug(
                    "overlapping_start_to_new_start: %s", overlapping_start_to_new_start
                )
                logging.debug(
                    "new_start_to_overlapping_end: %s", new_start_to_overlapping_end
                )
                logging.debug("new_start_to_new_end: %s", new_start_to_new_end)
                logging.debug(
                    "new_end_to_overlapping_end: %s", new_end_to_overlapping_end
                )
                logging.debug(
                    "overlapping_end_to_new_end: %s", overlapping_end_to_new_end
                )
                if overlapping_start_to_new_start > datetime.timedelta(0):
                    logging.debug("left side is positive")
                    overlapping_left_side = ContributionRange.objects.create(
                        user=user,
                        start_date=overlapping_range_start_date,
                        end_date=start_date - datetime.timedelta(days=1),
                    )
                    logging.info(
                        "created new range for overlapping left hand side %s from %s to %s",
                        overlapping_left_side,
                        overlapping_range_start_date,
                        start_date - datetime.timedelta(days=1),
                    )
                    add_contributions(contributions, overlapping_left_side)
                    ranges.append(overlapping_left_side)
                    filled_ranges.append(
                        (
                            overlapping_left_side.start_date,
                            overlapping_left_side.end_date,
                        )
                    )

                # middle
                if overlapping_range_start_date <= start_date:
                    logging.debug("middle point is new start date")
                    middle_start = start_date
                else:
                    logging.debug("middle point is overlapping start date")
                    middle_start = overlapping_range_start_date
                middle_start_to_overlapping_end = (
                    overlapping_range_end_date - middle_start
                )
                middle_start_to_new_end = end_date - middle_start
                middle_end = min(
                    middle_start_to_overlapping_end, middle_start_to_new_end
                )
                logging.debug(
                    "middle_start_to_overlapping_end: %s",
                    middle_start_to_overlapping_end,
                )
                logging.debug("middle_start_to_new_end: %s", middle_start_to_new_end)
                logging.debug("middle_end: %s", middle_end)
                if middle_end > datetime.timedelta(0):  # Has to always be true
                    logging.debug("middle_end is positive")
                    middle = ContributionRange.objects.create(
                        user=user,
                        start_date=middle_start,
                        end_date=middle_start + middle_end,
                    )
                    logging.info(
                        "created new range for overlapping middle %s from %s to %s",
                        middle,
                        middle_start,
                        middle_end,
                    )
                    add_contributions(contributions, middle)
                    ranges.append(middle)
                    filled_ranges.append((middle.start_date, middle.end_date))
                else:
                    logging.warning("middle_end is negative: %s", middle_end)

                # right side
                if new_end_to_overlapping_end > datetime.timedelta(0):
                    logging.debug("right side is positive")
                    overlapping_right_side = ContributionRange.objects.create(
                        user=user,
                        start_date=end_date + datetime.timedelta(days=1),
                        end_date=overlapping_range_end_date,
                    )
                    logging.info(
                        "created new range for overlapping right hand side %s from %s to %s",
                        overlapping_right_side,
                        end_date + datetime.timedelta(days=1),
                        overlapping_range_end_date,
                    )
                    add_contributions(contributions, overlapping_right_side)
                    ranges.append(overlapping_right_side)
                    filled_ranges.append(
                        (
                            overlapping_right_side.start_date,
                            overlapping_right_side.end_date,
                        )
                    )
                result += ranges

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
        return f"{self.goal}: {self.date_range.start_date} - {self.date_range.end_date} - {self.percentage}%"

    def validate_percentage(self):
        """
        The percentages of ALL user contributions for a given month cannot sum to more than 100
        """
        if not self.pk:
            total_existing_percentage = self.date_range.total_percentage
        else:
            # if update, we need to exclude the current contribution from the total
            total_existing_percentage = (
                self.date_range.contributions.exclude(id=self.id).aggregate(
                    models.Sum("percentage")
                )["percentage__sum"]
                or 0
            )
        if total_existing_percentage + self.percentage > 100:
            raise django.core.exceptions.ValidationError(
                f"Percentages cannot sum to more than 100. Total existing percentage: {total_existing_percentage}, new percentage: {self.percentage}"
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
        # if self.goal.is_finalized:
        #     raise django.core.exceptions.ValidationError(
        #         "Goal is already completed. Cannot create or update contributions."
        #     )
        if (
            self.date_range.contributions.filter(goal=self.goal)
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "A contribution for this goal already exists for this date range."
            )
        self.validate_range()
        self.validate_percentage()
        super().save(*args, **kwargs)

    def finalize(self, remaining_amount):
        """
        Calculate the total for this contribution, and set the amount.
        if total is larger than remaining_amount, set amount to remaining_amount.
        If total is less than remaining_amount, lower the percentage to match the total.
        """
        total = self.contribution
        if total > remaining_amount:
            self.amount = remaining_amount
            transactions_net_amount = total * 100 / self.percentage
            # we want to find min_percent so transactions_net_amount * min_percent / 100 = remaining
            minimum_required_percentage = (
                remaining_amount * 100 / transactions_net_amount
            )
            self.percentage = min(minimum_required_percentage, self.percentage)
        else:
            self.amount = total
        self.save()
        return self.amount

    @property
    def contribution(self):
        """
        Calculate how much was contributed to the goal for this contribution
        """
        if self.amount:
            return self.amount
        return self.date_range.transactions_net_amount * decimal.Decimal(
            self.percentage / 100
        )

    class Meta:
        """
        Meta class for goal contribution
        """

        verbose_name_plural = "goal contributions"
