from typing import Optional, Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View

from .forms import PupilSearchForm, PupilCreationForm, TaskSearchForm
from .models import TaskType, Task, EducationalStage, Pupil


@login_required
def index(request):
    """View function for the home page of the site."""

    num_tasks = Task.objects.count()
    num_educational_stages = EducationalStage.objects.count()
    num_task_types = TaskType.objects.count()
    task_types = TaskType.objects.all()
    stages = EducationalStage.objects.all()

    context = {
        "num_tasks": num_tasks,
        "num_educational_stages": num_educational_stages,
        "num_task_types": num_task_types,
        "task_types": task_types,
        "stages": stages
    }

    return render(request, "task_tracker/index.html", context=context)


class PupilListView(LoginRequiredMixin, generic.ListView):
    model = Pupil
    paginate_by = 3

    def get_context_data(
            self,
            *,
            object_list: Optional[list[Any]] = None,
            **kwargs,
    ) -> dict:
        context = super(PupilListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = PupilSearchForm(initial={"username": username})

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Pupil.objects.all()
        form = PupilSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return queryset


class PupilDetailView(LoginRequiredMixin, generic.DetailView):
    model = Pupil
    queryset = Pupil.objects.prefetch_related("tasks__task_type")
    template_name = "task_tracker/pupil_detail.html"


class PupilCreateView(LoginRequiredMixin, generic.CreateView):
    model = Pupil
    form_class = PupilCreationForm
    template_name = "task_tracker/pupil_form.html"
    success_url = reverse_lazy("task_tracker:pupil-list")


class PupilUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Pupil
    form_class = PupilCreationForm
    template_name = "task_tracker/pupil_form.html"
    success_url = reverse_lazy("task_tracker:pupil-list")


class PupilDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Pupil
    template_name = "task_tracker/pupil_delete.html"
    success_url = reverse_lazy("task_tracker:pupil-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "task_list"
    template_name = "task_tracker/task_list.html"
    paginate_by = 3

    def get_context_data(
            self,
            *,
            object_list: Optional[list[Any]] = None,
            **kwargs
    ) -> dict:
        context = super(TaskListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TaskSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.prefetch_related("assignees").select_related("task_type")

        form = TaskSearchForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "task_tracker/task_detail.html"


class TaskUpdateCompletionView(LoginRequiredMixin, View):
    def get(self, request, pk) -> HttpResponse:
        task = Task.objects.get(id=pk)
        task.is_completed = not task.is_completed
        task.save()
        context = {
            "task": task
        }
        return render(request, "task_tracker/task_detail.html", context=context)

    def post(self, request, pk) -> HttpResponse:
        task = Task.objects.get(id=pk)
        task.is_completed = request.POST.get("is_completed", not task.is_completed)
        task.save()
        context = {
            "task": task
        }
        return render(request, "task_tracker/task_detail.html", context=context)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = "__all__"
    template_name = "task_tracker/task_form.html"
    success_url = reverse_lazy("task_tracker:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    template_name = "task_tracker/task_form.html"
    success_url = reverse_lazy("task_tracker:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "task_tracker/task_delete.html"
    success_url = reverse_lazy("task_tracker:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task_type_list"
    template_name = "task_tracker/task_type_list.html"
    paginate_by = 3


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_tracker/task_type_form.html"
    success_url = reverse_lazy("task_tracker:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_tracker/task_type_form.html"
    success_url = reverse_lazy("task_tracker:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_tracker/task_type_delete.html"
    success_url = reverse_lazy("task_tracker:task-type-list")


class EducationalStageListView(LoginRequiredMixin, generic.ListView):
    model = EducationalStage
    context_object_name = "educational_stage_list"
    template_name = "task_tracker/educational_stage_list.html"
    paginate_by = 3


class EducationalStageCreateView(LoginRequiredMixin, generic.CreateView):
    model = EducationalStage
    fields = "__all__"
    template_name = "task_tracker/educational_stage_form.html"
    success_url = reverse_lazy("task_tracker:educational-stage-list")


class EducationalStageUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = EducationalStage
    fields = "__all__"
    template_name = "task_tracker/educational_stage_form.html"
    success_url = reverse_lazy("task_tracker:educational-stage-list")


class EducationalStageDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = EducationalStage
    template_name = "task_tracker/educational_stage_delete.html"
    success_url = reverse_lazy("task_tracker:educational-stage-list")
