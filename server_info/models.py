# -*- coding: utf-8 -*-
from django.db import models

class table(models.Model):
    IDC = models.CharField(verbose_name='机房', max_length=32, blank=True)
    position = models.CharField(verbose_name='机柜', max_length=32, blank=True)
    application = models.CharField(verbose_name='应用', max_length=128, blank=True)
    external_IP = models.GenericIPAddressField(verbose_name='外部IP', null=True)
    ssh_port = models.IntegerField(verbose_name='ssh端口', blank=True, null=True)
    inner_IP_1 = models.GenericIPAddressField(verbose_name='内部IP_1', null=True)
    inner_IP_2 = models.GenericIPAddressField(verbose_name='内部IP_2', null=True)
    manage_IP = models.GenericIPAddressField(verbose_name='内部IP_2', null=True)
    root_pass = models.CharField(verbose_name='root密码', max_length=32, blank=True)
    ubuntu_pass = models.CharField(verbose_name='ubuntu密码', max_length=32, blank=True)
    comment_1 = models.CharField(verbose_name='备注_1', max_length=128, blank=True)
    comment_2 = models.CharField(verbose_name='备注_2', max_length=128, blank=True)
    comment_3 = models.CharField(verbose_name='备注_3', max_length=128, blank=True)
    comment_4 = models.CharField(verbose_name='备注_4', max_length=128, blank=True)


class server_table(models.Model):
    class_1 = models.CharField(verbose_name='类型1', max_length=32, blank=True)
    class_2 = models.CharField(verbose_name='类型2', max_length=32, blank=True)
    class_3 = models.CharField(verbose_name='类型3', max_length=32, blank=True)
    login_ip = models.GenericIPAddressField(verbose_name='登录IP', null=True)
    ssh_port = models.IntegerField(verbose_name='ssh端口', blank=True, null=True)
    external_IP = models.GenericIPAddressField(verbose_name='外部IP', null=True)
    inner_ip_1 = models.GenericIPAddressField(verbose_name='内部IP_1', null=True)
    inner_ip_2 = models.GenericIPAddressField(verbose_name='内部IP_2', null=True)
    root_password = models.CharField(verbose_name='root密码', max_length=32, blank=True)
    ubuntu_password = models.CharField(verbose_name='ubuntu密码', max_length=32, blank=True)
    db_password = models.CharField(verbose_name='ubuntu密码', max_length=32, blank=True)
    description = models.CharField(verbose_name='功能描述', max_length=256, blank=True)
    manage_ip = models.GenericIPAddressField(verbose_name='管理IP', null=True)
    server_id = models.CharField(verbose_name='服务器ID', max_length=64, blank=True)
    comment_1 = models.CharField(verbose_name='备注_1', max_length=128, blank=True)
    comment_2 = models.CharField(verbose_name='备注_2', max_length=128, blank=True)
    IDC = models.CharField(verbose_name='机房', max_length=32, blank=True)
    position = models.CharField(verbose_name='机柜', max_length=32, blank=True)
    owner = models.CharField(verbose_name='机柜', max_length=32, blank=True)


class domain_name_CRT(models.Model):
    name_server = models.CharField(verbose_name='域名', max_length=32, blank=True)
    apply_time = models.DateField(verbose_name='申请时间', null=True)
    name_server_expiration_time = models.DateField(verbose_name='域名过期时间', null=True)
    CRT_expiration_time = models.DateField(verbose_name='证书过期时间', null=True)
    DNSPOD = models.CharField(verbose_name='DNSPOD', max_length=32, blank=True)
    account = models.CharField(verbose_name='账号', max_length=32, blank=True)
    comment = models.CharField(verbose_name='备注', max_length=32, blank=True)
    ICP = models.CharField(verbose_name='ICP备案号', max_length=32, blank=True)



class service_id(models.Model):
    service_name = models.CharField(verbose_name='服务名', max_length=32, blank=True)
    service_id = models.CharField(verbose_name='服务ID', max_length=16, blank=True)
    service_module = models.CharField(verbose_name='服务模块', max_length=16, blank=True)