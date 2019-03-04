# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def java_info_table(request):
    # flag = check_permission(u'nagios',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'java_info/java_info_table.html',{'user':request.user.username,
                                                     'path1':'monitor',
                                                     'path2':path,
                                                     'page_name1':u'java项目',
                                                     'page_name2':'java项目表'})