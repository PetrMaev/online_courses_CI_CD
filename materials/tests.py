from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import CustomUser


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="tester@sky.pro")
        self.course = Course.objects.create(
            title="Программирование",
            description="Курс по программированию",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            title="Python-разработчик",
            description="Урок Python-разработчик",
            course=self.course,
            video_link="https://www.youtube.com/",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование просмотра урока."""
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тестирование создания урока."""
        url = reverse("materials:lesson_create")
        data = {
            "title": "Java-разработчик",
            "description": "Урок Java-разработчик",
            "course": self.course.pk,
            "video_link": "https://www.youtube.com/dsfsdfsfsfs/",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тестирование изменения урока."""

        url = reverse("materials:lesson_edit", args=(self.lesson.pk,))

        data = {"video_link": "https://www.youtube.com/12345"}

        response = self.client.patch(url, data)

        self.assertEqual(data.get("video_link"), "https://www.youtube.com/12345")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        """Тестирование удаления урока."""

        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование вывода списка уроков."""
        url = reverse("materials:lesson_list")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "amount": None,
                    "preview": None,
                    "is_paid": False,
                    "stripe_product_id": None,
                    "video_link": self.lesson.video_link,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="tester@sky.pro")
        self.course = Course.objects.create(
            title="Веб-дизайн", description="Курс по веб-дизайну", owner=self.user, updated_at=None
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тестирование просмотра курса."""
        url = reverse("materials:courses-detail", args=(self.course.pk,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        """Тестирование создания курса."""
        url = reverse("materials:courses-list")
        data = {
            "title": "Кулинарные курсы",
            "description": "Курс по азиатской кухне",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """Тестирование изменения курса."""

        url = reverse("materials:courses-detail", args=(self.course.pk,))

        data = {
            "description": "Курс по паназиатской кухне",
        }

        response = self.client.patch(url, data)

        self.assertEqual(data.get("description"), "Курс по паназиатской кухне")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_delete(self):
        """Тестирование удаления курса."""

        url = reverse("materials:courses-detail", args=(self.course.pk,))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """Тестирование вывода списка курсов."""
        url = reverse("materials:courses-list")

        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "amount": None,
                    "description": "Курс по веб-дизайну",
                    "id": 4,
                    "is_subscribe": False,
                    "lesson_count": 0,
                    "lessons": [],
                    "title": "Веб-дизайн",
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscribeTestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email="tester@sky.pro")
        self.course = Course.objects.create(
            title="Веб-дизайн",
            description="Курс по веб-дизайну",
            is_subscribe=False,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_create(self):
        """Тестирование подписки на курс."""
        url = reverse("materials:course_subscribe", args=(self.course.pk,))

        response = self.client.post(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("message"), "подписка добавлена")
