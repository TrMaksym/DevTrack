from django.db import models
from django.contrib.auth.models import AbstractUser

class TaskType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)
    team_lead = models.ForeignKey("Worker", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name



class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position.name if self.position else "No Position"})"



class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name



class Task(models.Model):
    PRIORITY_CHOICES = [
        ("URG", "Urgent"),
        ("HI", "High"),
        ("MD", "Medium"),
        ("LO", "Low"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=3, choices=PRIORITY_CHOICES, default="MD")
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True, blank=True)
    assignees = models.ManyToManyField(Worker, related_name="tasks")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.name
