from django.conf.urls.static import static
from django.urls import path

from DivTrack import settings
from . import views

app_name = "TaskTracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("task_list/", views.task_list, name="task_list"),
    path("create_task/", views.create_task, name="create_task"),
    path("update_task/<int:task_id>/", views.update_task, name="update_task"),
    path("delete_task/<int:task_id>/", views.delete_task, name="delete_task"),
    path("project_list/", views.project_list, name="project_list"),
    path("create_project/", views.create_project, name="create_project"),
    path("update_project/<int:project_id>", views.update_project, name="update_project"),
    path("delete_project/<int:project_id>", views.delete_project, name="delete_project"),
    path("team_list/", views.team_list, name="team_list"),

]