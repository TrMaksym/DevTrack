from django.contrib import admin
from .models import Worker, Position, Project, Task, Team

class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "task_type", "priority", "is_completed", "project", "deadline")
    list_filter = ("is_completed", "priority", "task_type")
    search_fields = ("name", "description")

class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "position")
    list_filter = ("position",)
    search_fields = ("first_name", "last_name", "position__name")

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "end_date", "description")
    list_filter = ("start_date", "end_date")
    search_fields = ("name", "description")

class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "leader")
    search_fields = ("name",)

admin.site.register(Position, PositionAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Worker, WorkerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Team, TeamAdmin)
