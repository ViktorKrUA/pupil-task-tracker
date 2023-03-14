from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_tracker.forms import PupilCreationForm, TaskForm
from task_tracker.models import EducationalStage, TaskType


class FormsTests(TestCase):
    def test_pupil_creation_form_with_attributes_is_valid(self):
        educational_stage = EducationalStage.objects.create(name="test stage")
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "educational_stage": educational_stage,
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = PupilCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivatePupilTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
        self.stage = EducationalStage.objects.create(name="test stage")

    def test_create_pupil(self):
        form_data = {
            "username": "new_user",
            "educational_stage": self.stage.id,
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "user123test",
            "password2": "user123test",
        }
        self.client.post(reverse("task_tracker:pupil-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])


class PrivateTaskFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="test task type")

    def test_invalid_form(self):
        form_data = {
            "name": "",
            "description": "test description",
            "deadline": "",
            "task_type": self.task_type.id,
            "assignees": []
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("deadline", form.errors)
