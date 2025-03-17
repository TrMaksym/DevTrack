from django.contrib.auth.models import AbstractUser
from django.db import models

class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TaskType(models.Model):
    """Типи завдань (Bug, New feature, Breaking change)"""
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="workers",
        null=True
    )

    class Meta:
        ordering = ["position"]

    def __str__(self) -> str:
        position_name = self.position.name if self.position else "No Position"
        return f"{self.first_name} {self.last_name} ({position_name})"


class Task(models.Model):
    """Основна сутність - завдання"""
    PRIORITY_CHOICES = [
        ("U", "Urgent"),
        ("H", "High"),
        ("M", "Medium"),
        ("L", "Low"),
        ("B", "Backlog"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default="M")
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    created_by = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="created_tasks")

    class Meta:
        ordering = ["is_completed", "priority", "deadline"]

    def __str__(self) -> str:
        return self.name
