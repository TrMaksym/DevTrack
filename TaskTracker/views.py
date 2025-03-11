from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from TaskTracker.forms import ProjectForm
from TaskTracker.models import Project, Task


def index(request):
    return render(request, "TaskTracker/index.html")


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "TaskTracker/task_list.html", {"tasks": tasks})


def create_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        project_id = request.POST.get("id")
        assignee_id = request.POST.get("assignee")
        deadline = request.POST.get("deadline")

        project = Project.objects.get(id=project_id)
        assignee = User.objects.get(id=assignee_id) if assignee_id else None

        Task.objects.create(
            title=title,
            description=description,
            project=project,
            assignee=assignee,
            deadline=deadline,
        )
        return redirect("TaskTracker:task_list")

    projects = Project.objects.all()
    users = User.objects.all()
    return render(request, "TaskTracker/create_task.html", {"projects": projects, "users": users})


def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        project_id = request.POST.get("project")
        assignee_id = request.POST.get("assignee")
        deadline = request.POST.get("deadline")

        project = Project.objects.get(id=project_id)
        assignee = User.objects.get(id=assignee_id) if assignee_id else None

        task.project = project
        task.assignee = assignee
        task.deadline = deadline
        task.save()
        return redirect("TaskTracker:task_list")

    projects = Project.objects.all()
    users = User.objects.all()

    return render(request, "TaskTracker/update_task.html", {"task": task, "projects": projects, "users": users})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("TaskTracker:task_list")
    return render(request, "TaskTracker/delete_task.html", {"task": task})


def project_list(request):
    projects = Project.objects.all()
    return render(request, "TaskTracker/project_list.html", {"projects": projects})

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("TaskTracker:project_list")
    else:
        form = ProjectForm()

    return render(request, "TaskTracker/create_project.html", {"form": form})


def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("TaskTracker:project_list")
    else:
        form = ProjectForm(instance=project)

    return render(request, "TaskTracker/update_project.html", {"form": form, "project": project})


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("TaskTracker:project_list")

    return render(request, "TaskTracker/delete_project.html", {"project": project})


def team_list(request):
    return render(request, "TaskTracker/team_list.html")

