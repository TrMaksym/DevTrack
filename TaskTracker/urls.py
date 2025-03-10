from django.urls import path
from . import views

app_name = "TaskTracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("task_list/", views.task_list, name="task_list"),
    path("project_list/", views.project_list, name="project_list"),
    path("team_list/", views.team_list, name="team_list"),
]