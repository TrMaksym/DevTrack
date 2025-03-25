from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import (
    AboutUsView,
    TeamListView,
    WorkerDeleteView,
    WorkerUpdateView,
    WorkerCreateView,
    WorkerListView,
    TeamDeleteView,
    TeamUpdateView,
    TeamCreateView,
    PositionCreateView,
    ProjectCreateView,
    TaskTypeListView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDetailView,
    TaskTypeDeleteView, TeamDetailView, WorkerDetailView, ProjectUpdateView, ProjectDeleteView, ProjectDetailView,
    ProjectListView, TaskListView, TaskDetailView, TaskDeleteView, TaskUpdateView, TaskCreateView, PositionListView,
    PositionUpdateView, PositionDeleteView
)

app_name = "TaskTracker"


urlpatterns = [
    path("", views.index, name="index"),

    path("task-type-list/", TaskTypeListView.as_view(), name="task_type_list"),
    path("task-type/create/", TaskTypeCreateView.as_view(), name="task_type_create"),
    path("task-type/<int:pk>/update/", TaskTypeUpdateView.as_view(), name="task_type_update"),
    path("task-type/<int:pk>/detail/", TaskTypeDetailView.as_view(), name="task_type_detail"),
    path("task-type-delete/<int:pk>/", TaskTypeDeleteView.as_view(), name="task_type_delete"),

    path("task-list/", TaskListView.as_view(), name="task_list"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("task/<int:pk>/detail", TaskDetailView.as_view(), name="task_detail"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),
    path("worker/<int:pk>/detail/", WorkerDetailView.as_view(), name="worker-detail"),

    path("teams/", TeamListView.as_view(), name="team-list"),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path("team/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("team/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),
    path("team/<int:pk>/detail", TeamDetailView.as_view(), name="team_detail"),

    path("position/create", PositionCreateView.as_view(), name="position_create"),
    path("position/", PositionListView.as_view(), name="position_list"),
    path("position/<int:pk>/update/", PositionUpdateView.as_view(), name="position_update"),
    path("position/<int:pk>/delete/", PositionDeleteView.as_view(), name="position_delete"),

    path("project/", ProjectListView.as_view(), name="project_list"),
    path("project-create/", ProjectCreateView.as_view(), name="project_create"),
    path("project/<int:pk>/update/", ProjectUpdateView.as_view(), name="project_update"),
    path("project/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project_delete"),
    path("project/<int:pk>/detail/", ProjectDetailView.as_view(), name="project_detail"),

    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("about/", AboutUsView.as_view(), name='about-us'),

]