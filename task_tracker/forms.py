from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


from task_tracker.models import Pupil, Task


class PupilCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Pupil
        fields = UserCreationForm.Meta.fields + (
            "educational_stage",
            "first_name",
            "last_name",
        )


class PupilSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class TaskForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by task name"}),
    )
