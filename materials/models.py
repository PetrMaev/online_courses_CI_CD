from django.db import models
from django.core.validators import URLValidator


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/images/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )
    is_subscribe = models.BooleanField(default=False, verbose_name=r"Подписка на курс активна\неактивна")
    amount = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Стоимость",
        help_text="Укажите стоимость",
    )
    is_paid = models.BooleanField(default=False)
    stripe_product_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID курса на страйпе")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=225, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(
        upload_to="materials/images/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение",
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс обучения")
    video_link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        validators=[URLValidator(schemes="https")],
        verbose_name="Ссылка на видео",
    )
    owner = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )
    amount = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Стоимость",
        help_text="Укажите стоимость",
    )
    is_paid = models.BooleanField(default=False)
    stripe_product_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID урока на страйпе")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscribe(models.Model):
    user = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Название курса"
    )

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
