# Generated by Django 5.0.3 on 2024-03-25 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0011_alter_task_subtask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subtask',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='kanban.subtask'),
        ),
    ]
