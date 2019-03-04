# Generated by Django 2.0.6 on 2018-07-17 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='command_template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=32, unique=True, verbose_name='描述')),
                ('cmd', models.CharField(max_length=1024, verbose_name='命令')),
            ],
        ),
        migrations.CreateModel(
            name='server_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(max_length=32, unique=True, verbose_name='服务器名')),
                ('external_ip', models.CharField(max_length=64, verbose_name='外部IP')),
                ('os', models.CharField(max_length=64, verbose_name='系统')),
            ],
        ),
    ]
