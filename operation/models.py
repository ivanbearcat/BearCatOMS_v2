# -*- coding: utf-8 -*-
from django.db import models

class server_list(models.Model):
    server_name = models.CharField(verbose_name='服务器名', max_length=128, blank=False, unique=True)
    external_ip = models.GenericIPAddressField(verbose_name='外部IP')
    root_pass = models.CharField(verbose_name='root密码', max_length=32, blank=False)
    ssh_port = models.IntegerField(verbose_name='ssh端口', blank=True, null=True)
    os = models.CharField(verbose_name='系统', max_length=16, blank=False)

class command_template(models.Model):
    description = models.CharField(verbose_name='描述', max_length=32, blank=False, unique=True)
    cmd = models.CharField(verbose_name='命令', max_length=1024, blank=False)