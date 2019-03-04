# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def zabbix(request):
    # flag = check_permission(u'nagios',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'monitor/zabbix.html',{'user':request.user.username,
                                                     'path1':'monitor',
                                                     'path2':path,
                                                     'page_name1':u'监控',
                                                     'page_name2':'zabbix'})

@login_required
def zabbix_guild(request):
    # flag = check_permission(u'zabbix',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'monitor/zabbix_guild.html',{'user':request.user.username,
                                                     'path1':'monitor',
                                                     'path2':path,
                                                     'page_name1':u'监控',
                                                     'page_name2':'zabbix_guild'})


@login_required
def grafana(request):
    # flag = check_permission(u'zabbix',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'monitor/grafana.html',{'user':request.user.username,
                                                     'path1':'monitor',
                                                     'path2':path,
                                                     'page_name1':u'监控',
                                                     'page_name2':'grafana'})
