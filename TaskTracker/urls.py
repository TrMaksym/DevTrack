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
    TeamCreateView, PositionCreateView, ProjectCreateView
)

app_name = "TaskTracker"

urlpatterns = [
    path("", views.index, name="index"),

    path("task-type-list/", views.TaskTypeListView.as_view(), name="task_type_list"),
    path("task-type/create/", views.TaskTypeCreateView.as_view(), name="task_type_create"),
    path("task-type/<int:pk>/update/", views.TaskTypeUpdateView.as_view(), name="task_type_update"),
    path("task-type/<int:pk>/", views.TaskTypeDetailView.as_view(), name="task_type_detail"),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("worker/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),

    path("teams/", TeamListView.as_view(), name="team-list"),
    path("team/create/", TeamCreateView.as_view(), name="team-create"),
    path("team/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("team/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),

    path("position/", PositionCreateView.as_view(), name="position_create"),

    path("project-create/", ProjectCreateView.as_view(), name="project_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name='logout'),

    path("about-us/", AboutUsView.as_view(), name="about_us"),

]