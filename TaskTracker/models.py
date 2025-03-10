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
    teams = models.ManyToManyField("Team", related_name="team_members", blank=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="worker_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_query_name="worker",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="worker_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="worker",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})" if self.position else f"{self.first_name} {self.last_name}"


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    teams = models.ManyToManyField("Team", related_name="projects")

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    leader = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="leading_teams")
    members = models.ManyToManyField(Worker, related_name="worker_team", blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField(null=True, blank=True)
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
