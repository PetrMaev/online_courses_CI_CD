from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscribeAPIView,
)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lesson/<int:pk>/edit/", LessonUpdateAPIView.as_view(), name="lesson_edit"),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
    path("courses/<int:pk>/subscribe/", SubscribeAPIView.as_view(), name="course_subscribe"),
] + router.urls
