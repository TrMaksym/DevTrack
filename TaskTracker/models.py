from django.db import models
from django.contrib.auth.models import AbstractUser


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class TaskType(models.TextChoices):
    NONE = "", "None"
    BUG = "Bug", "Bug"
    NEW_FEATURE = "New feature", "New feature"
    BREAKING_CHANGE = "Breaking change", "Breaking change"
    REFACTORING = "Refactoring", "Refactoring"
    QA = "QA", "QA"


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    teams = models.ManyToManyField("Team", related_name="members", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})" if self.position else f"{self.first_name} {self.last_name}"


# Модель для проєкту (Project)
class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    teams = models.ManyToManyField("Team", related_name="projects")

    def __str__(self):
        return self.name


# Модель для команди (Team)
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    leader = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="leading_teams")
    members = models.ManyToManyField(Worker, related_name="teams", blank=True)

    def __str__(self):
        return self.name


# Модель для завдання (Task)
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=[("Urgent", "Urgent"), ("High", "High"), ("Medium", "Medium"), ("Low", "Low")],
        default="Medium"
    )
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.NONE
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(Worker)

    def __str__(self):
        return self.name
