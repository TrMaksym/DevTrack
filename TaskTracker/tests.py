from TaskTracker.models import Task, TaskType, Team, Project, Worker

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from TaskTracker.models import Project


class ProjectDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Test Team")
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.project = Project.objects.create(
            name="Test Project",
            description="Test Project Description",
            team=cls.team,
            deadline="2025-12-31"
        )

    def test_project_detail_view_with_permission(self):
        self.client.login(username="testuser", password="password")
        url = reverse("TaskTracker:project_detail", kwargs={"pk": self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TaskTracker/project_detail.html")
        self.assertEqual(response.context["project"], self.project)

    def test_project_detail_view_without_permission(self):
        url = reverse("TaskTracker:project_detail", kwargs={'pk': self.project.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TaskViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.worker = Worker.objects.create_user(
            username="testuser",
            password="password",
            first_name="Test",
            last_name="User"
        )
        cls.team = Team.objects.create(name="Test Team")
        cls.team.members.add(cls.worker)
        cls.project = Project.objects.create(
            name="Test Project",
            description="Test Project Description",
            deadline="2025-12-31",
            team=cls.team
        )
        cls.task_type = TaskType.objects.create(name="Test Task Type")

        cls.task = Task.objects.create(
            name="Test Task",
            project=cls.project,
            task_type=cls.task_type,
            priority="MD",
            team=cls.team,
            deadline="2025-12-31",
            description="Task Description"
        )
        cls.task.assignees.add(cls.worker)

    def setUp(self):
        logged_in = self.client.login(username="testuser", password="password")
        if not logged_in:
            print("Failed to log in!")

    def test_task_detail_view(self):
        url = reverse("TaskTracker:task_detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TaskTracker/task_detail.html")
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)

    def test_task_create_view(self):
        url = reverse("TaskTracker:task_create")
        data = {
            "name": "New Test Task",
            "description": "This is a new test task.",
            "project": self.project.pk,
            "task_type": self.task_type.pk,
            "priority": "MD",
            "team": self.team.pk,
            "deadline": "2025-12-31",
            "assignees": [self.worker.pk]
        }
        response = self.client.post(url, data)

        if response.status_code != 302:
            print("Response status code:", response.status_code)
            print("Form errors:", response.context.get("form").errors)
            print("Response content:", response.content.decode())
        self.assertEqual(response.status_code, 302, "Response didn't redirect as expected")
        self.assertRedirects(response, reverse("TaskTracker:task_detail", kwargs={"pk": Task.objects.last().pk}))
        self.assertEqual(Task.objects.count(), 2)

    def test_task_delete_view(self):
        url = reverse("TaskTracker:task-delete", kwargs={"pk": self.task.pk})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("TaskTracker:task_list"))
        self.assertEqual(Task.objects.count(), 0)

    def test_task_list_view(self):
        url = reverse("TaskTracker:task_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TaskTracker/task_list.html")
        self.assertContains(response, self.task.name)
        self.assertQuerySetEqual(response.context["tasks"], [self.task])