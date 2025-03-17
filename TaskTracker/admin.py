from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Position, TaskType, Team, Worker, Task


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "team_lead", "get_number_of_members",)

    def get_number_of_members(self, obj):
        return obj.members.count()
    get_number_of_members.short_description = "Number of members"


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = (
        "username",
        "get_full_name",
        "email",
        "position",
    )
    search_fields = ("username", "first_name", "last_name", "position__name")
    ordering = ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional information",
            {
                "fields": ("position", "team"),
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional information",
            {
                "fields": (
                    "first_name", "last_name", "email", "position", "team"
                ),
            },
        ),
    )

    def get_full_name(self, obj) -> str:
        return f"{obj.first_name} {obj.last_name}"

    get_full_name.short_description = "full_name"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "deadline", "priority", "is_completed", "task_type")
    search_fields = ("name", "task_type__name")
