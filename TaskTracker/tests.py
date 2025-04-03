from TaskTracker.models import Task, TaskType, Team, Project, Worker, Position

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ProjectDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Test Team")
        cls.worker = Worker.objects.create_user(username="testworker", password="password")
        cls.project = Project.objects.create(
            name="Test Project",
            description="Test Project Description",
            team=cls.team,
            deadline="2025-12-31"
        )

    def test_project_detail_view_with_permission(self):
        login_success = self.client.login(username="testworker", password="password")
        self.assertTrue(login_success, "Cant login to project")
        url = reverse("TaskTracker:project_detail", kwargs={"pk": self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TaskTracker/project_detail.html")

    def test_project_detail_view_without_permission(self):
        url = reverse("TaskTracker:project_detail", kwargs={'pk': self.project.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

class ProjectListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Test Team")
        cls.worker = Worker.objects.create_user(username="testworker_projectlist", password="password")  # Виправили username
        for i in range(20):
            Project.objects.create(
                name=f"Test Project {i}",
                description="Test Project Description",
                team=cls.team,
                deadline="2025-12-31"
            )

    def test_project_list_view_with_permission(self):
        self.client.login(username="testworker_projectlist", password="password")
        url = reverse("TaskTracker:project_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 15)
        self.assertTemplateUsed(response, "TaskTracker/project_list.html")
        self.assertContains(response, "Test Project 0")

    def test_project_list_view_search(self):
        self.client.login(username="testworker_projectlist", password="password")
        url = reverse("TaskTracker:project_list") + "?name=Test Project 1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertEqual(object_list.count(), 11)
        for project in object_list:
            self.assertIn("Test Project 1", project.name)

    def test_project_list_view_pagination(self):
        self.client.login(username="testworker_projectlist", password="password")
        url = reverse("TaskTracker:project_list") + "?page=2"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 5)

    def test_project_list_view_without_permission(self):
        url = reverse("TaskTracker:project_list")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

class ProjectUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Test Team")
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            team=cls.team,
            deadline="2025-12-31"
        )

    def test_project_update_view_with_permission(self):
        self.client.login(username="testuser", password="password")
        url = reverse("TaskTracker:project_update", kwargs={"pk": self.project.pk})
        data = {
            "name": "Updated Project",
            "description": "Updated Description",
            "team": self.team.pk,
            "deadline": "2026-01-01"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Updated Project")
        self.assertRedirects(response, reverse("TaskTracker:project_detail", kwargs={"pk": self.project.pk}))

    def test_project_update_view_without_permission(self):
        url = reverse("TaskTracker:project_update", kwargs={"pk": self.project.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class ProjectDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Test Team")
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            team=cls.team,
            deadline="2025-12-31"
        )

    def test_project_delete_view_with_permission(self):
        self.client.login(username="testuser", password="password")
        url = reverse("TaskTracker:project_delete", kwargs={"pk": self.project.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
        self.assertRedirects(response, reverse("TaskTracker:project_list"))

    def test_project_delete_view_without_permission(self):
        url = reverse("TaskTracker:project_delete", kwargs={"pk": self.project.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class ProjectCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Test Team")
        cls.user = Worker.objects.create_user(username="testuser_projectcreate", password="password")

    def test_project_create_view_with_permission(self):
        self.client.login(username="testuser_projectcreate", password="password")
        url = reverse("TaskTracker:project_create")
        data = {
            "name": "New Project",
            "description": "New Project Description",
            "team": self.team.pk,
            "deadline": "2025-12-31",
            "priority": "Medium",
            "status": "Pending"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        new_project = Project.objects.get(name="New Project")
        self.assertRedirects(response, reverse("TaskTracker:project_detail", kwargs={"pk": new_project.pk}))

    def test_project_create_view_without_permission(self):
        url = reverse("TaskTracker:project_create")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_project_create_view_invalid_deadline(self):
        self.client.login(username="testuser_projectcreate", password="password")
        url = reverse("TaskTracker:project_create")
        data = {
            "name": "Invalid Project",
            "description": "Invalid Deadline",
            "team": self.team.pk,
            "deadline": "2020-01-01",  # Минула дата
            "priority": "Medium",
            "status": "Pending"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The deadline must be in the future")


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


class WorkerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.team = Team.objects.create(name="Test Team")
        cls.position = Position.objects.create(name="Developer")
        cls.admin_position = Position.objects.create(name="admin")
        cls.user = Worker.objects.create_user(username="testuser", password="password")

        cls.worker = Worker.objects.create_user(
            username="worker1",
            first_name="First1",
            last_name="Last1",
            password="password",
            position=cls.position
        )

        for i in range(2, 21):
            Worker.objects.create_user(
                username=f"worker{i}",
                first_name=f"First{i}",
                last_name=f"Last{i}",
                password="password",
                position=cls.position
            )

        Worker.objects.create_user(
            username="adminuser",
            password="password",
            position=cls.admin_position
        )

    def test_worker_list_view_the_permission(self):
        self.client.login(username="testuser", password="password")
        url = reverse("TaskTracker:worker-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 15)
        self.assertTemplateUsed(response, "TaskTracker/worker_list.html")
        self.assertNotIn("adminuser", [w.username for w in response.context["object_list"]])

    def test_worker_list_view_search_single_word(self):
        self.client.login(username="testuser", password="password")
        url = reverse("TaskTracker:worker-list") + "?search=First1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertTrue(object_list.count() > 0)
        for worker in object_list:
            self.assertIn("First1", worker.first_name)

    def test_worker_list_view_search_multiple_words(self):
        self.client.login(username="testuser", password="password")
        url = reverse("TaskTracker:worker-list") + "?search=First1 Last1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertEqual(object_list.count(), 1)
        worker = object_list[0]
        self.assertEqual(worker.first_name, "First1")
        self.assertEqual(worker.last_name, "Last1")

    def test_worker_list_view_search_three_words(self):
        self.client.login(username="testuser", password="password")
        url = reverse("TaskTracker:worker-list") + "?search=First1 Last1 Developer"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertEqual(object_list.count(), 1)
        worker = object_list[0]
        self.assertEqual(worker.first_name, "First1")
        self.assertEqual(worker.last_name, "Last1")
        self.assertEqual(worker.position.name, "Developer")

    def test_worker_list_view_without_permission(self):
        url = reverse("TaskTracker:worker-list")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TeamListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.team_lead = Worker.objects.create_user(
            username="teamlead_teamlist",
            password="password",
            position=cls.position
        )
        cls.user = Worker.objects.create_user(
            username="testuser_teamlist",
            password="password"
        )

        for i in range(15):
            team = Team.objects.create(
                name=f"Team {i}",
                team_lead=cls.team_lead
            )
            for j in range(2):
                member = Worker.objects.create_user(
                    username=f"member_teamlist_{i}_{j}",
                    password="password",
                    position=cls.position
                )
                team.members.add(member)

    def test_team_list_view_with_permission(self):
        self.client.login(username="testuser_teamlist", password="password")
        url = reverse("TaskTracker:team-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["object_list"]), 10)
        self.assertTemplateUsed(response, "TaskTracker/team_list.html")
        for team in response.context["object_list"]:
            self.assertEqual(team.member_count, 2)

    def test_team_list_view_search(self):
        self.client.login(username="testuser_teamlist", password="password")
        url = reverse("TaskTracker:team-list") + "?search=Team 1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context["object_list"]
        self.assertEqual(object_list.count(), 6)
        for team in object_list:
            self.assertIn("Team 1", team.name)

    def test_team_list_view_without_permission(self):
        url = reverse("TaskTracker:team-list")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TeamDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.team_lead = Worker.objects.create_user(
            username="teamlead_teamdetail",
            password="password",
            position=cls.position
        )
        cls.user = Worker.objects.create_user(
            username="testuser_teamdetail",
            password="password"
        )
        cls.team = Team.objects.create(name="Test Team", team_lead=cls.team_lead)
        cls.member = Worker.objects.create_user(
            username="member_teamdetail_1",
            password="password",
            position=cls.position
        )
        cls.team.members.add(cls.member)

    def test_team_detail_view_with_permission(self):
        self.client.login(username="testuser_teamdetail", password="password")
        url = reverse("TaskTracker:team_detail", kwargs={"pk": self.team.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TaskTracker/team_detail.html")
        self.assertEqual(response.context["team"], self.team)

    def test_team_detail_view_without_permission(self):
        url = reverse("TaskTracker:team_detail", kwargs={"pk": self.team.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TeamCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.team_lead = Worker.objects.create_user(
            username="teamlead_teamcreate",
            password="password",
            position=cls.position
        )
        cls.user = Worker.objects.create_user(
            username="testuser_teamcreate",
            password="password"
        )

    def test_team_create_view_with_permission(self):
        self.client.login(username="testuser_teamcreate", password="password")
        url = reverse("TaskTracker:team-create")
        data = {
            "name": "New Team",
            "team_lead": self.team_lead.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        new_team = Team.objects.get(name="New Team")
        self.assertEqual(new_team.team_lead, self.team_lead)
        self.assertRedirects(response, reverse("TaskTracker:team_detail", kwargs={"pk": new_team.pk}))

    def test_team_create_view_without_permission(self):
        url = reverse("TaskTracker:team-create")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TeamUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.team_lead = Worker.objects.create_user(
            username="teamlead_teamupdate",
            password="password",
            position=cls.position
        )
        cls.user = Worker.objects.create_user(
            username="testuser_teamupdate",
            password="password"
        )
        cls.team = Team.objects.create(name="Test Team", team_lead=cls.team_lead)

    def test_team_update_view_with_permission(self):
        self.client.login(username="testuser_teamupdate", password="password")
        url = reverse("TaskTracker:team-update", kwargs={"pk": self.team.pk})
        data = {
            "name": "Updated Team",
            "team_lead": self.team_lead.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, "Updated Team")
        self.assertRedirects(response, reverse("TaskTracker:team_detail", kwargs={"pk": self.team.pk}))

    def test_team_update_view_without_permission(self):
        url = reverse("TaskTracker:team-update", kwargs={"pk": self.team.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TeamDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.team_lead = Worker.objects.create_user(
            username="teamlead_teamdelete",
            password="password",
            position=cls.position
        )
        cls.user = Worker.objects.create_user(
            username="testuser_teamdelete",
            password="password"
        )
        cls.team = Team.objects.create(name="Test Team", team_lead=cls.team_lead)

    def test_team_delete_view_with_permission(self):
        self.client.login(username="testuser_teamdelete", password="password")
        url = reverse("TaskTracker:team-delete", kwargs={"pk": self.team.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Team.objects.filter(pk=self.team.pk).exists())
        self.assertRedirects(response, reverse("TaskTracker:team-list"))

    def test_team_delete_view_without_permission(self):
        url = reverse("TaskTracker:team-delete", kwargs={"pk": self.team.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TaskTypeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(name="Developer")
        cls.user = Worker.objects.create_user(
            username="testuser_tasktypelist",
            password="password",
            position=cls.position
        )
        cls.team = Team.objects.create(
            name="Test Team",
            team_lead=cls.user
        )
        cls.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
            deadline="2025-12-31",
            team=cls.team
        )
        for i in range(15):
            task_type = TaskType.objects.create(name=f"Task Type {i}")
            for j in range(2):
                task = Task.objects.create(
                    name=f"Task {i}{j}",
                    description="Test Task",
                    deadline="2025-12-31",
                    task_type=task_type,
                    project=cls.project,
                    team=cls.team
                )
                task.assignees.set([cls.user])

    def test_task_type_list_view_with_permission(self):
        self.client.login(username="testuser_tasktypelist", password="password")
        url = reverse("TaskTracker:task_type_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["task_type_list"]), 10)
        self.assertTemplateUsed(response, "TaskTracker/task_type_list.html")
        for task_type in response.context["task_type_list"]:
            self.assertEqual(task_type.task_count, 2)

    def test_task_type_list_view_search(self):
        self.client.login(username="testuser_tasktypelist", password="password")
        url = reverse("TaskTracker:task_type_list") + "?search=Task Type 1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        object_list = response.context["task_type_list"]
        self.assertEqual(object_list.count(), 6)
        for task_type in object_list:
            self.assertIn("Task Type 1", task_type.name)

    def test_task_type_list_view_without_permission(self):
        url = reverse("TaskTracker:task_type_list")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TaskTypeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Worker.objects.create_user(
            username="testuser_tasktypedetail",
            password="password",
        )
        cls.task_type = TaskType.objects.create(name="Task Type")

    def test_task_type_detail_view_with_permission(self):
        self.client.login(username="testuser_tasktypedetail", password="password")
        url = reverse("TaskTracker:task_type_detail", kwargs={"pk": self.task_type.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TaskTracker/task_type_detail.html")
        self.assertEqual(response.context["task_type"], self.task_type)

    def test_task_type_detail_view_without_permission(self):
        url = reverse("TaskTracker:task_type_detail", kwargs={"pk": self.task_type.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TaskTypeCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Worker.objects.create_user(
            username="testuser_tasktypecreate",
            password="password"
        )

    def test_task_type_create_view_with_permission(self):
        self.client.login(username="testuser_tasktypecreate", password="password")
        url = reverse("TaskTracker:task_type_create")
        data = {"name": "New Task Type"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("TaskTracker:task_type_list"))

    def test_task_type_create_view_without_permission(self):
        url = reverse("TaskTracker:task_type_create")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class TaskTypeUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Worker.objects.create_user(
            username="testuser_tasktypeupdate",
            password="password"
        )
        cls.task_type = TaskType.objects.create(name="Test Task Type")

    def test_task_type_update_view_with_permission(self):
        self.client.login(username="testuser_tasktypeupdate", password="password")
        url = reverse("TaskTracker:task_type_update", kwargs={"pk": self.task_type.pk})
        data = {"name": "Updated Task Type"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Updated Task Type")
        self.assertRedirects(response, reverse("TaskTracker:task_type_detail", kwargs={"pk": self.task_type.pk}))

    def test_task_type_update_view_without_permission(self):
        url = reverse("TaskTracker:task_type_update", kwargs={"pk": self.task_type.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

class TaskTypeDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Worker.objects.create_user(
            username="testuser_tasktypedelete",
            password="password"
        )
        cls.task_type = TaskType.objects.create(name="Test Task Type")

    def test_task_type_delete_view_with_permission(self):
        self.client.login(username="testuser_tasktypedelete", password="password")
        url = reverse("TaskTracker:task_type_delete", kwargs={"pk": self.task_type.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("TaskTracker:task_type_list"))

    def test_task_type_delete_view_without_permission(self):
        url = reverse("TaskTracker:task_type_delete", kwargs={"pk": self.task_type.pk})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

class PositionListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            Position.objects.create(name=f"Position {i}")

    def test_position_list_view(self):
        url = reverse("TaskTracker:position_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "TaskTracker/position_list.html")
        self.assertEqual(len(response.context["position_list"]), 5)


class PositionCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Worker.objects.create_user(
            username="testuser_positioncreate",
            password="password"
        )

    def test_position_create_view_with_permission(self):
        self.client.login(username="testuser_positioncreate", password="password")
        url = reverse("TaskTracker:position_create")
        data = {"name": "New Position"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("TaskTracker:position_list"))

    def test_position_create_view_without_permission(self):
        url = reverse("TaskTracker:position_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PositionUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Worker.objects.create_user(
            username="testuser_positionupdate",
            password="password"
        )
        cls.position = Position.objects.create(name="Test Position")

    def test_position_update_view_with_permission(self):
        self.client.login(username="testuser_positionupdate", password="password")
        url = reverse("TaskTracker:position_update", kwargs={"pk": self.position.pk})
        data = {"name": "Updated Position"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Updated Position")
        self.assertRedirects(response, reverse("TaskTracker:position_list"))

    def test_position_update_view_without_permission(self):
        url = reverse("TaskTracker:position_update", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PositionDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Worker.objects.create_user(
            username="testuser_positiondelete",
            password="password"
        )
        cls.position = Position.objects.create(name="Test Position")

    def test_position_delete_view_with_permission(self):
        self.client.login(username="testuser_positiondelete", password="password")
        url = reverse("TaskTracker:position_delete", kwargs={"pk": self.position.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(pk=self.position.pk).exists())
        self.assertRedirects(response, reverse("TaskTracker:position_list"))

    def test_position_delete_view_without_permission(self):
        url = reverse("TaskTracker:position_delete", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)