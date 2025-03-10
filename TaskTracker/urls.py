from django.urls import path

from . import views

app_name = "TaskTracker"

urlpatterns = [
    path("", views.index, name="index"),

]
