from django.urls import path

from users.apps import UsersConfig
from users.views import (
    PaymentsCourseCreateAPIView,
    PaymentsDestroyAPIView,
    PaymentsListAPIView,
    PaymentsRetrieveAPIView,
    PaymentsUpdateAPIView,
    CustomUserCreateAPIView,
    CustomUserListAPIView,
    CustomUserRetrieveAPIView,
    CustomUserUpdateAPIView,
    CustomUserDestroyAPIView,
    PaymentsLessonCreateAPIView,
    PaymentsCourseCheckoutSessionAPIView,
    PaymentsLessonCheckoutSessionAPIView,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [
    path("users/create/", CustomUserCreateAPIView.as_view(), name="user_create"),
    path("users/", CustomUserListAPIView.as_view(), name="user_list"),
    path("users/<int:pk>/", CustomUserRetrieveAPIView.as_view(), name="user_detail"),
    path("users/<int:pk>/edit/", CustomUserUpdateAPIView.as_view(), name="user_edit"),
    path("users/delete/<int:pk>/", CustomUserDestroyAPIView.as_view(), name="user_delete"),
    path("payments/course/create/", PaymentsCourseCreateAPIView.as_view(), name="payment_course_create"),
    path("payments/lesson/create/", PaymentsLessonCreateAPIView.as_view(), name="payment_lesson_create"),
    path("payments/", PaymentsListAPIView.as_view(), name="payments_list"),
    path("payments/<int:pk>/", PaymentsRetrieveAPIView.as_view(), name="payment_detail"),
    path("payments/course/<int:pk>/", PaymentsCourseCheckoutSessionAPIView.as_view(), name="payment_course_check"),
    path("payments/lesson/<int:pk>/", PaymentsLessonCheckoutSessionAPIView.as_view(), name="payment_lesson_check"),
    path("payments/<int:pk>/edit/", PaymentsUpdateAPIView.as_view(), name="payment_edit"),
    path("payments/delete/<int:pk>/", PaymentsDestroyAPIView.as_view(), name="payment_delete"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
