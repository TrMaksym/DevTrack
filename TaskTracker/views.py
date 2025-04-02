from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import ListView, TemplateView

from .forms import ProjectSearchForm, WorkerSearchForm, TaskSearchForm, PositionForm, TaskTypeSearchForm, TeamListForm, \
    ProjectForm
from .models import TaskType, Position, Team, Worker, Project, Task



@login_required
def index(request):
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()
    num_projects = Project.objects.count()
    num_tasks = Task.objects.count()
    context = {
        "num_teams": num_teams,
        "num_workers": num_workers,
        "num_projects": num_projects,
        "num_tasks": num_tasks,
    }
    return render(request, "TaskTracker/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "TaskTracker/task_type_list.html"
    context_object_name = "task_type_list"
    queryset = TaskType.objects.annotate(task_count=Count("task")).order_by("name")
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TaskTypeSearchForm(self.request.GET)
        return context


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    template_name = "TaskTracker/task_type_detail.html"
    context_object_name = "task_type"


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "TaskTracker/task_type_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:task_type_list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "TaskTracker/task_type_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:task_type_detail", kwargs={"pk": self.object.pk})


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    context_object_name = "task_type"
    success_url = reverse_lazy("TaskTracker:task_type_list")
    template_name = "TaskTracker/task_type_confirm_delete.html"


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    queryset = Team.objects.select_related("team_lead").annotate(member_count=Count("members")).order_by("name")
    paginate_by = 10
    template_name = "TaskTracker/team_list.html"

    def get_queryset(self):
        search_query = self.request.GET.get('search', "")
        queryset = super().get_queryset()
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TeamListForm(self.request.GET)
        return context


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    template_name = "TaskTracker/team_detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("members", "projects")


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    fields = "__all__"
    template_name = "TaskTracker/team_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:team_detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    fields = "__all__"
    template_name = "TaskTracker/team_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:team_detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("TaskTracker:team-list")
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
    template_name = "TaskTracker/worker_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("team", "position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position", "team", "phone_number", "address", "date_of_birth")
    template_name = "TaskTracker/worker_form.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(self.request.POST['password'])
        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("TaskTracker:worker_detail", kwargs={"pk": self.object.pk})


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position", "team", "phone_number", "address", "date_of_birth")
    template_name = "TaskTracker/worker_form.html"

    def form_valid(self, form):
        if 'password' in self.request.POST:
            user = form.save(commit=False)
            user.set_password(self.request.POST['password'])
            user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("TaskTracker:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("TaskTracker:worker-list")
    template_name = "TaskTracker/worker_confirm_delete.html"


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 15
    template_name = "TaskTracker/project_list.html"

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
    template_name = "TaskTracker/project_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("team")


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ProjectForm
    model = Project
    template_name = "TaskTracker/project_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:project_detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProjectForm
    model = Project
    template_name = "TaskTracker/project_form.html"


    def get_success_url(self):
        return reverse_lazy("TaskTracker:project_detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("TaskTracker:project_list")
    template_name = "TaskTracker/project_confirm_delete.html"


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "TaskTracker/task_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("project", "team", "task_type")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "TaskTracker/task_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = None
        return context

    def get_success_url(self):
        return reverse_lazy("TaskTracker:task_detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    template_name = "TaskTracker/task_form.html"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:task_detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("TaskTracker:task_list")
    template_name = "TaskTracker/task_confirm_delete.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "TaskTracker/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            priority = form.cleaned_data.get("priority")
            if name:
                queryset = queryset.filter(name__icontains=name)
            if priority:
                queryset = queryset.filter(priority=priority)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskSearchForm(self.request.GET)
        return context


class AboutUsView(TemplateView):
    template_name = 'about-us.html'

class PositionCreateView(generic.CreateView):
    model = Position
    fields = ['name']
    template_name = 'TaskTracker/position_form.html'
    success_url = reverse_lazy('TaskTracker:position_list')

class PositionListView(generic.ListView):
    model = Position
    template_name = "TaskTracker/position_list.html"
    context_object_name = "positions"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class PositionUpdateView(generic.UpdateView):
    model = Position
    form_class = PositionForm
    template_name = "TaskTracker/position_update.html"
    context_object_name = "position"

    def get_success_url(self):
        return reverse_lazy("TaskTracker:position_list")


class PositionDeleteView(generic.DeleteView):
    model = Position
    template_name = "TaskTracker/position_delete.html"
    context_object_name = "position"
    success_url = reverse_lazy("TaskTracker:position_list")
