from django.core.management.base import BaseCommand, CommandError
from goal.models import Goal, GoalRecurranceType, GoalStatus
import datetime


class Command(BaseCommand):
    help = "Create goals for all recurring goals"

    def handle(self, *args, **options):
        # get all goals with recurring set to FIXED OR INDEFINITE
        # AND no goal has it as a previous goal
        predecessor_goals = Goal.objects.all().values_list("previous_goal", flat=True)
        print(predecessor_goals)
        goals = Goal.objects.filter(
            recurring__in=[GoalRecurranceType.FIXED, GoalRecurranceType.INDEFINITE]
        )
        for goal in goals:
            if goal.id in predecessor_goals:
                continue
            if datetime.date.today() - goal.expected_completion_date < datetime.timedelta(
                months=goal.reccuring_frequency
            ):
                continue
            start_date = goal.expected_completion_date + datetime.timedelta(days=1)
            end_date = start_date + goal.expected_completion_date - goal.start_date
            new_goal = Goal.objects.create(
                user=goal.user,
                amount=goal.amount,
                recurring=goal.recurring,
                reccuring_frequency=goal.reccuring_frequency,
                start_date=start_date,
                expected_completion_date=end_date,
                previous_goal=goal,
                status=GoalStatus.IN_PROGRESS,
            )
            new_goal.save()
