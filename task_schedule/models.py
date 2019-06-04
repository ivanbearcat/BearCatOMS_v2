# -*- coding: utf-8 -*-
from django.db import models

class single_tasks(models.Model):
    task_name = models.CharField(max_length=64, unique=True)
    task_desc = models.CharField(max_length=128)
    task_type = models.CharField(max_length=16)
    target = models.CharField(max_length=32)
    task_cmd = models.TextField(max_length=65525)
    duration = models.CharField(max_length=32)
    status = models.CharField(max_length=16)
    pods_name = models.CharField(max_length=128)
    task_id = models.CharField(max_length=64, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    last_run_time = models.DateTimeField(null=True)

class task_group(models.Model):
    group_name = models.CharField(max_length=64, unique=True)
    group_desc = models.CharField(max_length=128)
    group_content = models.TextField(max_length=65525)
    duration = models.CharField(max_length=32)
    status = models.CharField(max_length=16)
    task_now = models.CharField(max_length=64)
    task_id = models.CharField(max_length=64, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    last_run_time = models.DateTimeField(null=True)

