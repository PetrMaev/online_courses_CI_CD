from config import settings
from celery import shared_task
from django.core.mail import send_mail

from materials.models import Course


@shared_task
def send_email_course_update(course_id: int) -> None:
    course = Course.objects.get(id=course_id)
    recipients = course.subscriptions.values_list("user__email", flat=True)
    send_mail(
        f"Обновления в курсе {course.title}",
        "Перейдите в личный кабинет, чтобы ознакомиться с обновлениями",
        settings.EMAIL_HOST_USER,
        recipients,
    )
