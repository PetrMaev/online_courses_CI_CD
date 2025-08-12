from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import Payments


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        Payments.objects.all().delete()

        call_command("loaddata", "payments_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
