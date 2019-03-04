# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from BearCatOMSv2.settings import logger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.db.models.query_utils import Q
from audit.models import log
from operation.models import server_list
from commons.get_client_ip import get_ip


@login_required
def audit_log(request):
    # flag = check_permission(u'操作日志',request.user.username)
    # if flag < 1:
    #     return render(request,request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'audit/audit_log.html',{'user':request.user.username,
                                                           'path1':'audit',
                                                           'path2':path,
                                                           'page_name1':u'运维审计',
                                                           'page_name2':u'操作日志'})

@login_required
def audit_log_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['application','username','command','time','id']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = log.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.all().count()
        else:
            result_data = log.objects.filter(Q(application__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.filter(Q(application__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                                 Q(id__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = log.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.all().count()
        else:
            result_data = log.objects.filter(Q(application__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = log.objects.filter(Q(application__contains=sSearch) | \
                                            Q(username__contains=sSearch) | \
                                            Q(command__contains=sSearch) | \
                                            Q(time__contains=sSearch) | \
                                                 Q(id__contains=sSearch)).count()
    for i in  result_data:
        aaData.append({
                       '0':i.application,
                       '1':i.username,
                       '2':i.command.replace('\n','</br>').replace(' ','&nbsp'),
                       '3':i.time,
                       '4':i.type,
                       '5':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")



@csrf_exempt
def audit_get_data(request):
    # orm = server_list.objects.all()
    # allow_ip_list = []
    # for i in orm:
    #     allow_ip_list.append(i.external_ip)
    # if get_ip(request) in allow_ip_list:
        application = request.POST.get('application')
        username = request.POST.get('username')
        command = request.POST.get ('command')
        time = request.POST.get ('time')
        _type = request.POST.get ('type')
        last_command = log.objects.filter(application=application).order_by('id').reverse()[:1]
        for i in last_command:
            if i.command == command:
                return HttpResponse('duplicate')
        if application and username and command and time and _type:
            try:
                log.objects.create(application=application,username=username,command=command,time=time,type=_type)
                return HttpResponse('success')
            except Exception as e:
                logger.error(e)
                return HttpResponse('error')
        else:
            return HttpResponse('error')
    # else:
    #     return HttpResponse('not allow')