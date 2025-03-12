from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from TaskTracker.forms import ProjectForm, TaskForm, TeamForm, TaskSearchForm, TeamSearchForm, ProjectSearchForm
from TaskTracker.models import Project, Task, Team, Worker


def index(request):
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits
    return render(request, "TaskTracker/index.html", {"num_visits": num_visits})

@login_required
def task_list(request):
    form = TaskSearchForm(request.GET)
    tasks = Task.objects.all().order_by("-deadline")

    if form.is_valid():
        title = form.cleaned_data.get("title")
        description = form.cleaned_data.get("description")
        if title:
            tasks = tasks.filter(title__icontains=title)
        if description:
            tasks = tasks.filter(description__icontains=description)

    paginator = Paginator(tasks, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "TaskTracker/task_list.html", {
        "form": form,
        "page_obj": page_obj
    })


@login_required
def create_task(request):
    projects = Project.objects.all()
    workers = Worker.objects.all()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)


            task.project = form.cleaned_data['project']
            task.save()

            assignees = form.cleaned_data['assignees']
            task.assignees.set(assignees)
            task.save()

            return redirect('TaskTracker:task_list')

    else:
        form = TaskForm()

    return render(request, "TaskTracker/create_task.html", {
        "form": form,
        "projects": projects,
        "workers": workers
    })



@login_required
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

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("TaskTracker:task_list")
    return render(request, "TaskTracker/delete_task.html", {"task": task})


@login_required
def project_list(request):
    form = ProjectSearchForm(request.GET or None)
    projects = Project.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')

        if name:
            projects = projects.filter(name__icontains=name)
        if description:
            projects = projects.filter(description__icontains=description)

    paginator = Paginator(projects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "TaskTracker/project_list.html", {
        "form": form,
        "projects": page_obj,
    })

@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("TaskTracker:project_list")
    else:
        form = ProjectForm()

    return render(request, "TaskTracker/create_project.html", {"form": form})

@login_required
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

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("TaskTracker:project_list")

    return render(request, "TaskTracker/delete_project.html", {"project": project})


@login_required
def team_list(request):
    form = TeamSearchForm(request.GET or None)

    teams = Team.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        if name:
            teams = teams.filter(name__icontains=name)

    paginator = Paginator(teams, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "TaskTracker/team_list.html", {
        "teams": page_obj,
        "form": form,  # передаємо форму в шаблон
    })


@login_required
def create_team(request):
    users = Worker.objects.all()

    if request.method == "POST":
        form = TeamForm(request.POST)

        if form.is_valid():
            team = form.save(commit=False)
            leader_id = form.cleaned_data.get('leader')
            if leader_id:
                team.leader = Worker.objects.get(id=leader_id)
            team.save()

            members = form.cleaned_data.get('members')
            team.members.set(members)

            return redirect('TaskTracker:team_list')

    else:
        form = TeamForm()

    return render(request, 'TaskTracker/create_team.html', {'form': form, 'users': users})

@login_required
def update_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('TaskTracker:team_list')
    else:
        form = TeamForm(instance=team)

    return render(request, 'TaskTracker/update_team.html', {'form': form, 'team': team})

@login_required
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.method == "POST":
        team.delete()
        return redirect("TaskTracker:team_list")

    return render(request, "TaskTracker/delete_team.html", {"team": team})

# class WorkerCreateView(LoginRequiredMixin, CreateView):
#     model = Worker
#     form_class = WorkerCreationForm
#     template_name = "TaskTracker/worker_form.html"
#     success_url = reverse_lazy("TaskTracker:worker_list")