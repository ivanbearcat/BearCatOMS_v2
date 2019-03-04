# -*- coding: utf-8 -*-
from django.db import models

class log(models.Model):
    application = models.CharField(verbose_name='应用', max_length=32, blank=False)
    username = models.CharField(verbose_name='用户名', max_length=32, blank=False)
    command = models.CharField(verbose_name='命令', max_length=256, blank=False)
    time = models.CharField(verbose_name='时间', max_length=32, blank=False)
    type = models.CharField(verbose_name='类型', max_length=16, blank=False)