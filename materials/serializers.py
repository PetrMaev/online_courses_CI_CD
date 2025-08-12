from rest_framework import serializers

from materials.models import Course, Lesson, Subscribe
from materials.validators import VideoLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [VideoLinkValidator(field="video_link")]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "is_subscribe",
            "amount",
            "updated_at",
            "lesson_count",
            "lessons",
        )


class SubscribeSerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Subscribe
        fields = (
            "id",
            "user",
            "course",
            "course_count",
            "courses",
        )
