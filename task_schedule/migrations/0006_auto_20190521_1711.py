# Generated by Django 2.0 on 2019-05-21 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_schedule', '0005_auto_20190521_1431'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='tasks',
            new_name='single_tasks',
        ),
    ]
