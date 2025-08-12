from django.core.management import call_command
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson, Subscribe


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Subscribe.objects.all().delete()

        call_command("loaddata", "course_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))

        call_command("loaddata", "lesson_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))

        call_command("loaddata", "subscribe_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
