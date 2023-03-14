from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from task_tracker.models import Task, TaskType, EducationalStage


class ModelsTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="test")
        self.assertEqual(str(task_type), f"{task_type.name}")

    def test_stage_str(self):
        stage = EducationalStage.objects.create(name="test")
        self.assertEqual(str(stage), f"{stage.name}")

    def test_task_str(self):
        task_type = TaskType.objects.create(name="test")
        europe_kiev = pytz.timezone('Europe/Kiev')
        task = Task.objects.create(
            name="test name",
            description="test description",
            priority="test",
            deadline=datetime(2024, 3, 5, 14, 30, tzinfo=europe_kiev),
            task_type=task_type
        )
        self.assertEqual(str(task), f"{task.name}")

    def test_pupil_str(self):

        pupil = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )
        self.assertEqual(
            str(pupil),
            f"{pupil.username} {pupil.first_name} {pupil.last_name}"
        )
