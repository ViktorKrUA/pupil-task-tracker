from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TaskType, EducationalStage, Pupil, Task


@admin.register(Pupil)
class PupilAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("educational_stage",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("educational_stage",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "educational_stage",
                    )
                }
            )
        )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("deadline", "priority", "task_type")


admin.site.register(TaskType)
admin.site.register(EducationalStage)
