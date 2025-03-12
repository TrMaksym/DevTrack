from datetime import date

import age
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Project, Task, TaskType, Team, Worker


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "assignees", "deadline", "task_type", "priority", "project"]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )
    task_type = forms.ChoiceField(
        choices=TaskType.choices,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    priority = forms.ChoiceField(
        choices=[("Urgent", "Urgent"), ("High", "High"), ("Medium", "Medium"), ("Low", "Low")],
        widget=forms.Select(attrs={"class": "form-control"})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )




class TeamForm(forms.ModelForm):
    leader = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    members = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"})
    )

    class Meta:
        model = Team
        fields = ["name", "leader", "members"]


class TaskSearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=100, required=False)


class ProjectSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="Search by Project Name")

class TeamSearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="Search by Team Name")


# class WorkerCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Worker
#         fields = UserCreationForm.Meta.fields + (
#             "first_name",
#             "last_name",
#             "email",
#             "position",
#             "teams"
#         )
#
# class WorkerForm(forms.ModelForm):
#     class Meta:
#         model = Worker
#         fields = ['first_name', 'last_name', 'username', 'email', 'position', 'teams']
