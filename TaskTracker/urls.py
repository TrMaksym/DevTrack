from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views


app_name = "TaskTracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("task-type/", views.TaskTypeListView.as_view(), name="task_type"),
    path("task-type/create/", views.TaskTypeCreateView.as_view(), name="task_type_create"),
    path("task-type/<int:pk>/update/", views.TaskTypeUpdateView.as_view(), name="task_type_update"),
    path("task-type/<int:pk>/", views.TaskTypeDetailView.as_view(), name="task_type_detail"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]