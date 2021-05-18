from django.db import models

class server(models.Model):
    class Meta:
        verbose_name_plural = "服务器"

    UUID = models.CharField(verbose_name='UUID', max_length=32, blank=True, null=True, unique=True)
    hostname = models.CharField(verbose_name='主机名', max_length=32, blank=True, null=True,)
    os = models.CharField(verbose_name='系统', max_length=16, blank=True, null=True,)
    kernel_version = models.CharField(verbose_name='内核版本', max_length=16, blank=True, null=True,)
    cpu_count = models.IntegerField(verbose_name='CPU数量', blank=True, null=True)
    cpu_model = models.CharField(verbose_name='CPU型号',  max_length=16, blank=True, null=True)
    cabinet_info = models.CharField(verbose_name='机柜信息',  max_length=128, blank=True, null=True)
    # server_group
    # disk
    # memory
    # NIC
    ssh_ip = models.GenericIPAddressField(verbose_name='SSH连接用IP', blank=True, null=True)
    ssh_port = models.IntegerField(verbose_name='ssh连接用端口', blank=True, null=True)
    ssh_user = models.CharField(verbose_name='SSH连接用账号', max_length=32, blank=True, null=True)
    ssh_pass = models.CharField(verbose_name='SSH连接用密码', max_length=32, blank=True, null=True)
    update_time = models.DateTimeField(verbose_name='最后更新时间', auto_now=True)
    comment =  models.CharField(verbose_name='备注', max_length=256, blank=True, null=True)

class disk(models.Model):
    class Meta:
        verbose_name_plural = "磁盘"

    name = models.CharField(verbose_name='磁盘名', max_length=32, blank=False, null=False)
    size = models.CharField(verbose_name='容量', max_length=16, blank=True, null=True)
    server = models.ForeignKey('server', on_delete=models.DO_NOTHING)

class memory(models.Model):
    class Meta:
        verbose_name_plural = "内存"

    slot = models.CharField(verbose_name='插槽', max_length=8, blank=False, null=False)
    model = models.CharField(verbose_name='型号', max_length=64, blank=True, null=True)
    size = models.CharField(verbose_name='容量', max_length=16, blank=True, null=True)
    sn = models.CharField(verbose_name='SN号', max_length=64, blank=True, null=True)
    server = models.ForeignKey('server', on_delete=models.DO_NOTHING)

class NIC(models.Model):
    class Meta:
        verbose_name_plural = "网卡"

    name = models.CharField(verbose_name='网卡名', max_length=16, blank=False, null=False)
    mac = models.CharField(verbose_name='MAC地址', max_length=32, blank=True, null=True)
    ipaddr = models.GenericIPAddressField(verbose_name='IP地址', blank=True, null=True)
    netmask = models.GenericIPAddressField(verbose_name='子网掩码', blank=True, null=True)
    server = models.ForeignKey('server', on_delete=models.DO_NOTHING)

class server_group(models.Model):
    class Meta:
        verbose_name_plural = "服务器组"

    name = models.CharField(verbose_name='组名', max_length=64, blank=True, null=True)
    server = models.ForeignKey('server', on_delete=models.DO_NOTHING)