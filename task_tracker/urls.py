from django.urls import path

from .views import (
    index,
    PupilListView,
    PupilDetailView,
    PupilCreateView,
    PupilUpdateView,
    PupilDeleteView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskTypeListView,
    TaskTypeDetailView,
    TaskTypeCreateView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    EducationalStageListView,
    EducationalStageCreateView,
    EducationalStageUpdateView,
    EducationalStageDeleteView,
)


urlpatterns = [
    path("", index, name="index"),
    path("pupils/", PupilListView.as_view(), name="pupil-list"),
    path("pupils/<int:pk>/", PupilDetailView.as_view(), name="pupil-detail"),
    path("pupils/create/", PupilCreateView.as_view(), name="pupil-create"),
    path(
        "pupils/<int:pk>/update/",
        PupilUpdateView.as_view(),
        name="pupil-update",
    ),
    path(
        "pupils/<int:pk>/delete/",
        PupilDeleteView.as_view(),
        name="pupil-delete",
    ),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete",
    ),
    path("task_types/", TaskTypeListView.as_view(), name="task-type-list"),
    path(
        "task_types/<int:pk>/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail",
    ),
    path(
        "task_types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path(
        "task_types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "task_types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
    path(
        "educational_stages/",
        EducationalStageListView.as_view(),
        name="educational-stage-list",
    ),
    path(
        "educational_stages/create/",
        EducationalStageCreateView.as_view(),
        name="educational-stage-create",
    ),
    path(
        "educational_stages/<int:pk>/update/",
        EducationalStageUpdateView.as_view(),
        name="educational-stage-update",
    ),
    path(
        "educationals_tages/<int:pk>/delete/",
        EducationalStageDeleteView.as_view(),
        name="educational-stage-delete",
    ),

]

app_name = "task_tracker"
