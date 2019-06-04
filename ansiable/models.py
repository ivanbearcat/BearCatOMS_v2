# -*- coding: utf-8 -*-
from django.db import models

class logs(models.Model):
    name = models.CharField(max_length=32)
    project_name = models.CharField(max_length=64)
    operation = models.CharField(max_length=10240)
    time = models.DateTimeField(auto_now_add=True)
