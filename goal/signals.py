from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Goal, GoalContribution, ContributionRange
from .utils import update_status, create_goals


@receiver(post_save, sender=Goal)
def on_goal_create(sender, instance, created, **_kwargs):
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


@receiver(post_delete, sender=GoalContribution)
def on_goal_contribution_delete(sender, instance, **_kwargs):
    """
    Re-assign contributions to other goals
    """
    # find all ranges associated with contribution
    instance.date_range.distribute_remaining_percentages()


@receiver(post_delete, sender=Goal)
def on_goal_delete(sender, instance, **_kwargs):
    """
    Delete all contributions and ranges associated with goal
    """
    # find all ranges with no other contributions
    contribution_ranges = ContributionRange.objects.filter(contributions__isnull=True)
    # delete all ranges
    contribution_ranges.delete()


@receiver(user_logged_in)
def on_user_login(sender, request, user, **_kwargs):
    """
    Update status of all goals
    Create new goals for all recurring goals
    TODO Use a daily cron job to update status and create goals
    """
    update_status(user)
    create_goals(user)
