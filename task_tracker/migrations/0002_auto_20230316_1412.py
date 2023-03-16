from django.db import migrations
from django.db.migrations import RunPython


def func(apps, schema_editor):
    from django.core.management import call_command
    call_command('loaddata', 'pupil_task_tracker_db_data.json')


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("task_tracker", "0001_initial"),
    ]

    operations = [RunPython(func, reverse_func)]
