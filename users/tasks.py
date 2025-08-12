from dateutil.relativedelta import relativedelta

from django.utils import timezone
from celery import shared_task

from users.models import CustomUser


@shared_task
def check_last_login_user():
    month_ago = timezone.now() - relativedelta(months=1)
    users = CustomUser.objects.filter(is_staff=False, is_superuser=False, is_active=True, last_login__lte=month_ago)
    users.update(is_active=False)
