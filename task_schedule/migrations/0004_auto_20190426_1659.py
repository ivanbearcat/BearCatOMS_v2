# Generated by Django 2.0 on 2019-04-26 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_schedule', '0003_auto_20190426_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='pods_name',
            field=models.CharField(max_length=128),
        ),
    ]
