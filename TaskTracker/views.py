from django.shortcuts import render

def index(request):
    return render(request, "TaskTracker/index.html")


def task_list(request):
    return render(request, "TaskTracker/task_list.html")


def project_list(request):
    return render(request, "TaskTracker/project_list.html")


def team_list(request):
    return render(request, "TaskTracker/team_list.html")