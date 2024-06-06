from django.core.management.base import BaseCommand, CommandError
from goal.utils import update_status


class Command(BaseCommand):
    help = "Update goal status"

    def handle(self, *args, **options):
        update_status()
        self.stdout.write(self.style.SUCCESS("Successfully updated goal status"))
