from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import ProjectSearchForm, WorkerSearchForm
from .models import TaskType, Position, Team, Worker, Project, Task



@login_required
def index(request):
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()
    num_projects = Project.objects.count()
    context = {
        "num_teams": num_teams,
        "num_workers": num_workers,
        "num_projects": num_projects,
    }
    return render(request, "TaskTracker/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "TaskTracker/task_type_list.html"
    context_object_name = "task_type_list"
    queryset = TaskType.objects.annotate(task_count=Count("tasks")).order_by("name")
    paginate_by = 15


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    template_name = "TaskTracker/task_type_detail.html"
    context_object_name = "task_type"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "TaskTracker/task_type_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:task-type-detail", kwargs={"pk": self.object.pk})


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "TaskTracker/task_type_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:task-type-detail", kwargs={"pk": self.object.pk})


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    context_object_name = "task_type"
    success_url = reverse_lazy("tasktracker:task-type-list")
    template_name = "TaskTracker/task_type_confirm_delete.html"


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    queryset = Team.objects.select_related("team_lead").annotate(member_count=Count("members")).order_by("name")
    paginate_by = 10


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_queryset(self):
        return super().get_queryset().prefetch_related("members", "projects")


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    template_name = "TaskTracker/team_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    template_name = "TaskTracker/team_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("tasktracker:team-list")
    template_name = "TaskTracker/team_confirm_delete.html"


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "")
        context["search"] = search
        context["search_form"] = WorkerSearchForm(initial={"search": search})
        return context

    def get_queryset(self):
        queryset = Worker.objects.exclude(position__name="admin").select_related("position")
        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            search_values = search_query.split()
            filters = Q()

            if len(search_values) == 1:
                filters |= Q(first_name__icontains=search_values[0])
                filters |= Q(last_name__icontains=search_values[0])
                filters |= Q(position__name__icontains=search_values[0])

            elif len(search_values) == 2:
                filters |= Q(first_name__icontains=search_values[0], last_name__icontains=search_values[1])
                filters |= Q(first_name__icontains=search_values[1], last_name__icontains=search_values[0])

            elif len(search_values) == 3:
                filters |= Q(first_name__icontains=search_values[0], last_name__icontains=search_values[1], position__name__icontains=search_values[2])
                filters |= Q(first_name__icontains=search_values[1], last_name__icontains=search_values[0], position__name__icontains=search_values[2])

            elif len(search_values) > 3:
                return Worker.objects.none()
            queryset = queryset.filter(filters)

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_queryset(self):
        return super().get_queryset().select_related("team", "position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position", "team")
    template_name = "TaskTracker/worker_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:worker-detail", kwargs={"pk": self.object.pk})


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position", "team")
    template_name = "TaskTracker/worker_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("tasktracker:worker-list")
    template_name = "TaskTracker/worker_confirm_delete.html"


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = ProjectSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return Project.objects.filter(name__icontains=form.cleaned_data["name"])
        return Project.objects.all()


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_queryset(self):
        return super().get_queryset().select_related("team")


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    template_name = "TaskTracker/project_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:project-detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"
    template_name = "TaskTracker/project_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("tasktracker:project-list")
    template_name = "TaskTracker/project_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Task.objects.all()


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        return super().get_queryset().select_related("project", "team", "task_type")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "TaskTracker/task_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:task-detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    template_name = "TaskTracker/task_form.html"

    def get_success_url(self):
        return reverse_lazy("tasktracker:task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasktracker:task-list")
    template_name = "TaskTracker/task_confirm_delete.html"
