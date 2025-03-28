from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Worker, Team, Project, Task, Position


class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email", "position", "team")


class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "team_lead", "members")


class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name", "team_lead", "members")

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
        team.members.set(self.cleaned_data["members"])
        team.team_lead = self.cleaned_data["team_lead"]
        return team


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput
        (attrs={
            'placeholder': 'Search by name'}
        )
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        empty_label="All Projects",
        label="Project"
    )


class WorkerSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search'}
        )
    )

class TaskSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search Task"})
    )
    priority = forms.ChoiceField(
        choices=[("", "All")] + Task.PRIORITY_CHOICES,
        required=False,
        label="Filter by Priority"
    )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']



class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']

class TaskTypeSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search Task Type"})
    )