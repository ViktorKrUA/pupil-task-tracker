from django.contrib.auth.models import AbstractUser
from django.db import models


class TaskType(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name


class EducationalStage(models.Model):
    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name


class Pupil(AbstractUser):
    educational_stage = models.ForeignKey(EducationalStage, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "pupil"
        verbose_name_plural = "pupils"

    def __str__(self) -> str:
        return f"{self.username} {self.first_name} {self.last_name}"


class Task(models.Model):
    PRIORITY_TYPES = (
        ("URGENT", "Urgent"),
        ("HIGH", "High"),
        ("MEDIUM", "Medium"),
        ("LOW", "Low"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(null=True, default=False)
    priority = models.CharField(max_length=6, choices=PRIORITY_TYPES, default="LOW")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(Pupil, related_name="tasks")

    def __str__(self) -> str:
        return self.name
