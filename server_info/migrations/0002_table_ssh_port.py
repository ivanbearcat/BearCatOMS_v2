# Generated by Django 2.0.6 on 2018-07-18 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='ssh_port',
            field=models.IntegerField(blank=True, null=True, verbose_name='ssh端口'),
        ),
    ]
