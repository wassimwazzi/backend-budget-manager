from django.core.management.base import BaseCommand, CommandError
from goal.models import Goal, GoalRecurranceType

class Command(BaseCommand):
    help = 'Create goals for all recurring goals'

    def handle(self, *args, **options):
        # get all goals with recurring set to FIXED OR INDEFINITE
        # AND no goal has it as a previous goal
        goals = Goal.objects.filter(recurring__in=[GoalRecurranceType.FIXED, GoalRecurranceType.INDEFINITE], previous_goal__isnull=True)