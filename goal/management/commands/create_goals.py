from django.core.management.base import BaseCommand
from goal.utils import create_goals


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


class Command(BaseCommand):
    help = "Create goals for all recurring goals"

    def handle(self, *args, **options):
        create_goals()
        self.stdout.write(self.style.SUCCESS("Successfully created goals"))
