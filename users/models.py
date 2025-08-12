from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )
    phone_number = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Введите свой номер телефона",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Страна",
        help_text="Укажите свою страну",
    )
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="Дата последней авторизации")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    CASH = "cash"
    TRANSFER = "transfer"

    METHOD_CHOICES = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        "materials.Course", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Оплаченный курс"
    )
    paid_lesson = models.ForeignKey(
        "materials.Lesson",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        related_name="lesson",
    )
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    pay_method = models.CharField(max_length=15, choices=METHOD_CHOICES, verbose_name="Способ оплаты")
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )
    payment_link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
