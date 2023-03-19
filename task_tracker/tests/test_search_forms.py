from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_tracker.models import Pupil, Task


class TestSearch(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user123"
        )
        self.client.force_login(self.user)

    def test_search_students_by_username(self):
        response = self.client.get(
            reverse("task_tracker:pupil-list") + "?username=user123"
        )
        self.assertEqual(
            list(response.context["pupil_list"]),
            list(Pupil.objects.filter(username__icontains="user123")),
        )

    def test_search_task_by_name(self):
        response = self.client.get(
            reverse("task_tracker:task-list") + "?name=write"
        )
        self.assertEqual(
            list(response.context["task_list"]),
            list(Task.objects.filter(name__icontains="write")),
        )
