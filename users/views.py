from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from users.models import CustomUser, Payments
from users.permissions import IsUserOwner
from users.serializers import CustomUserSerializer, PaymentsSerializer
from users.services import (
    create_stripe_course_product,
    create_stripe_price,
    create_stripe_session,
    create_stripe_lesson_product,
    checkout_course_session,
    convert_rub_to_usd,
)


# Пользователь
class CustomUserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class CustomUserListAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


class CustomUserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


class CustomUserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsUserOwner]


# Платежи
class PaymentsCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payments = serializer.save(user=self.request.user)
        course = get_object_or_404(Course, pk=payments.paid_course.id)
        course_product = create_stripe_course_product(payments.paid_course.id)
        course.stripe_product_id = course_product.get("id")
        course.save()
        price = create_stripe_price(payments.amount, course_product)
        session_id, payment_link = create_stripe_session(price)
        payments.session_id = session_id
        payments.payment_link = payment_link
        payments.save()


class PaymentsLessonCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payments = serializer.save(user=self.request.user)
        amount_in_usd = convert_rub_to_usd(payments.amount)
        lesson = get_object_or_404(Lesson, pk=payments.paid_lesson.id)
        lesson_product = create_stripe_lesson_product(payments.paid_lesson.id)
        lesson.stripe_product_id = lesson_product.get("id")
        lesson.save()
        price = create_stripe_price(amount_in_usd, lesson_product)
        session_id, payment_link = create_stripe_session(price)
        payments.session_id = session_id
        payments.payment_link = payment_link
        payments.save()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "pay_method",
    )
    ordering_fields = ("date",)
    permission_classes = [IsAuthenticated]


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsCourseCheckoutSessionAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self, **kwargs):
        payment_id = kwargs.get("id")
        payments = get_object_or_404(Payments, pk=payment_id)
        course = get_object_or_404(Course, pk=payments.paid_course.id)
        return checkout_course_session(course.pk, payments.session_id)


class PaymentsLessonCheckoutSessionAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self, **kwargs):
        payment_id = kwargs.get("id")
        payments = get_object_or_404(Payments, pk=payment_id)
        lesson = get_object_or_404(Lesson, pk=payments.paid_course.id)
        return checkout_course_session(lesson.pk, payments.session_id)


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]
