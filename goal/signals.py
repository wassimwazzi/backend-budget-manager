from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Goal, GoalContribution, ContributionRange


@receiver(post_save, sender=Goal)
def on_goal_create(sender, instance, created, **kwargs):
    """
    Create default contribution for goal
    """
    if not created:
        return

    ranges = ContributionRange.add_new_range(
        user=instance.user,
        start_date=instance.start_date,
        end_date=instance.expected_completion_date,
    )
    # create a contribution for each range, with max percentage possible
    for r in ranges:
        # keep only ranges that are within the goal's date range
        if not (
            r.start_date >= instance.start_date
            and r.end_date <= instance.expected_completion_date
        ):
            continue
        remaining_percentage = 100 - r.total_percentage
        GoalContribution.objects.create(
            goal=instance, percentage=remaining_percentage, date_range=r
        )


@receiver(post_delete, sender=Goal)
def on_goal_delete(sender, instance, **kwargs):
    """
    Delete all contributions and ranges associated with goal
    """
    # find all ranges with no other contributions
    contribution_ranges = ContributionRange.objects.filter(contributions__isnull=True)
    # delete all ranges
    contribution_ranges.delete()
