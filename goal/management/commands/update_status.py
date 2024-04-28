from django.core.management.base import BaseCommand, CommandError
from goal.models import Goal, GoalStatus
import datetime


class Command(BaseCommand):
    help = "Update goal status"

    def handle(self, *args, **options):
        # get all goals in progress or pending
        goals = Goal.objects.filter(
            status__in=[GoalStatus.IN_PROGRESS, GoalStatus.PENDING]
        )
        for goal in goals:
            if goal.expected_completion_date < datetime.date.today():
                goal.status = (
                    GoalStatus.COMPLETED if goal.progress == 100 else GoalStatus.FAILED
                )
                goal.save()
            elif goal.start_date < datetime.date.today():
                goal.status = GoalStatus.IN_PROGRESS
                goal.save()
            else:
                goal.status = GoalStatus.PENDING
                goal.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated goal status"))
