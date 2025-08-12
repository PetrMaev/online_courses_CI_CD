from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email="moder@sky.pro",
            first_name="Moder",
        )
        user.set_password("123qwe")
        user.is_active = True
        user.save()
        moderators_group = Group.objects.create(name="Moderators")
        user.groups.add(moderators_group)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created moderator user with email {user.email}"))
