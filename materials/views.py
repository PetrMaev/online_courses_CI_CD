from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscribe
from materials.paginators import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from materials.tasks import send_email_course_update
from users.permissions import IsModer, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)  # noqa: F841

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve", "list"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Moderators").exists():
            return queryset
        else:
            return queryset.filter(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        course_id = kwargs["pk"]
        course = get_object_or_404(Course, pk=course_id)
        last_updated = course.updated_at
        response = super().update(request, *args, **kwargs)
        course.refresh_from_db()
        if course.subscriptions.exists() and timezone.now() - last_updated > timedelta(hours=4):
            send_email_course_update.delay(course_id=course_id)
        return response


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)  # noqa: F841


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name="Moderators").exists():
            return queryset
        else:
            return queryset.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]


# Подписка
class SubscribeAPIView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModer]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = kwargs["pk"]
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscribe.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            subs_item.save()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            course_item.is_subscribe = True
            course_item.save()
            subscribe = Subscribe.objects.create(user=user, course=course_item)  # noqa: F841
            message = "подписка добавлена"
        # Возвращаем ответ в API
        return Response({"message": message})
