from django.core.management.base import BaseCommand, CommandError
from goal.models import Goal, GoalRecurranceType, GoalStatus
import datetime

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

class Command(BaseCommand):
    help = "Create goals for all recurring goals"

    def handle(self, *args, **options):
        # get all goals with recurring set to FIXED OR INDEFINITE
        # AND no goal has it as a previous goal
        predecessor_goals = Goal.objects.all().values_list("previous_goal__id", flat=True)
        goals = Goal.objects.filter(
            recurring__in=[GoalRecurranceType.FIXED, GoalRecurranceType.INDEFINITE],
        )#.exclude(id__in=predecessor_goals)
        print(predecessor_goals)
        print(goals)
        for goal in goals:
            if goal.id in predecessor_goals:
                continue
            if diff_month(datetime.date.today(), goal.expected_completion_date) <= goal.reccuring_frequency-1:
                continue
            start_date = goal.expected_completion_date + datetime.timedelta(days=1)
            goal_range = goal.expected_completion_date - goal.start_date
            end_date = start_date + goal_range
            new_goal = Goal.objects.create(
                user=goal.user,
                amount=goal.amount,
                recurring=goal.recurring,
                reccuring_frequency=goal.reccuring_frequency,
                start_date=start_date,
                expected_completion_date=end_date,
                previous_goal=goal,
                status=GoalStatus.IN_PROGRESS,
                description=goal.description,
            )
            new_goal.save()
