# Generated by Django 5.0.3 on 2024-03-25 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0007_alter_task_assigned_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assigned_users',
            field=models.ManyToManyField(blank=True, to='kanban.contact'),
        ),
    ]
