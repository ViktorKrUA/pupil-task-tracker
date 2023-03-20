from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_tracker.models import Task, TaskType, EducationalStage, Pupil

TASK_URL = reverse("task_tracker:task-list")
TASK_TYPE_URL = reverse("task_tracker:task-type-list")
PUPIL_URL = reverse("task_tracker:pupil-list")
STAGE_URL = reverse("task_tracker:educational-stage-list")


class PublicTaskTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(TASK_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTests(TestCase):
    def setUp(self) -> None:
        task_type = TaskType.objects.create(name="test")
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

        europe_kiev = pytz.timezone('Europe/Kiev')
        self.task = Task.objects.create(
            name="Test Task",
            description="Test description",
            task_type=task_type,
            deadline=datetime(2024, 3, 5, 14, 30, tzinfo=europe_kiev),
            is_completed=False
        )
        self.url = reverse("task_tracker:update-completion", kwargs={'pk': self.task.pk})

    def test_retrieve_tasks(self):
        Task(name="write an essay")
        Task(name="pass an exam")

        response = self.client.get(TASK_URL)

        tasks = Task.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"])[:3],
            list(tasks)[:3]
        )

        self.assertTemplateUsed(response, "task_tracker/task_list.html")

    def test_for_update_task_completion(self):
        # Initial check if task is not completed
        self.assertFalse(self.task.is_completed)

        # Testing if task is marked as completed if it wasn't
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)

        # Check for "Undo" button to make task not completed
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)

        self.task.refresh_from_db()
        self.assertFalse(self.task.is_completed)


class PublicStageTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(PUPIL_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateStageTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_stages(self):
        EducationalStage.objects.create(
            name="Test name"
        )

        response = self.client.get(STAGE_URL)

        stages = EducationalStage.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["educational_stage_list"])[:3],
            list(stages)[:3]
        )

        self.assertTemplateUsed(response, "task_tracker/educational_stage_list.html")


class PublicTaskTypeTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(STAGE_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_task_types(self):
        TaskType.objects.create(
            name="Test name"
        )

        response = self.client.get(TASK_TYPE_URL)

        types = TaskType.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_type_list"])[:3],
            list(types)[:3]
        )

        self.assertTemplateUsed(response, "task_tracker/task_type_list.html")


class PublicPupilTests(TestCase):
    def test_list_login_required(self):
        res = self.client.get(PUPIL_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivatePupilTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_pupils(self):
        Pupil.objects.create(
            username="Test username"
        )

        response = self.client.get(PUPIL_URL)

        pupil = Pupil.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["pupil_list"])[:3],
            list(pupil)[:3]
        )

        self.assertTemplateUsed(response, "task_tracker/pupil_list.html")
