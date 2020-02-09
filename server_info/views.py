# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from BearCatOMSv2.settings import logger
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from server_info.models import table, server_table, domain_name_CRT
import json

@login_required
def server_info_table(request):
    # if not request.user.has_perm('server_info.can_view'):
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'server_info/server_info_table.html',{'user':request.user.username,
                                                               'path1':'server_info',
                                                               'path2':path,
                                                               'page_name1':u'信息表',
                                                               'page_name2':u'服务器信息表(旧)'})



@login_required
def server_info_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    IDC = request.POST.get('IDC')

    aaData = []
    sort = ['IDC','position','application','external_IP','ssh_port','inner_IP_1','inner_IP_2','manage_IP','root_pass',
            'ubuntu_pass','comment_1','comment_2','comment_3','comment_4','id']

    if IDC == 'all':
        if  sSortDir_0 == 'asc':
            if sSearch == '':
                result_data = table.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.all().count()
            else:
                result_data = table.objects.filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)) \
                                                .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)).count()
        else:
            if sSearch == '':
                result_data = table.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.all().count()
            else:
                result_data = table.objects.filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)) \
                                                .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)).count()
    else:
        if  sSortDir_0 == 'asc':
            if sSearch == '':
                result_data = table.objects.filter(IDC=IDC).order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(IDC=IDC).count()
            else:
                result_data = table.objects.filter(IDC=IDC).filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)) \
                                                .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(IDC=IDC).filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)).count()
        else:
            if sSearch == '':
                result_data = table.objects.filter(IDC=IDC).order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(IDC=IDC).count()
            else:
                result_data = table.objects.filter(IDC=IDC).filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)) \
                                                .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
                iTotalRecords = table.objects.filter(IDC=IDC).filter(Q(IDC__contains=sSearch) | \
                                                   Q(application__contains=sSearch) | \
                                                   Q(external_IP__contains=sSearch) | \
                                                   Q(inner_IP_1__contains=sSearch) | \
                                                   Q(inner_IP_2__contains=sSearch) | \
                                                   Q(manage_IP__contains=sSearch) | \
                                                   Q(comment_1__contains=sSearch) | \
                                                   Q(comment_2__contains=sSearch) | \
                                                   Q(comment_3__contains=sSearch) | \
                                                   Q(comment_4__contains=sSearch) | \
                                                   Q(id__contains=sSearch)).count()

    for i in  result_data:
        aaData.append({
                       '0':i.IDC,
                       '1':i.position,
                       '2':i.application,
                       '3':i.external_IP,
                       '4':i.ssh_port,
                       '5':i.inner_IP_1,
                       '6':i.inner_IP_2,
                       '7':i.manage_IP,
                       '8':i.root_pass,
                       '9':i.ubuntu_pass,
                       '10':i.comment_1,
                       '11':i.comment_2,
                       '12':i.comment_3,
                       '13':i.comment_4,
                       '14':i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")



@login_required
def server_info_save(request):
    _id = request.POST.get('id')
    IDC = request.POST.get('IDC')
    position = request.POST.get('position')
    application = request.POST.get('application')
    external_IP = request.POST.get('external_IP')
    ssh_port = request.POST.get('ssh_port')
    inner_IP_1 = request.POST.get('inner_IP_1')
    inner_IP_2 = request.POST.get('inner_IP_2')
    manage_IP = request.POST.get('manage_IP')
    root_pass = request.POST.get('root_pass')
    ubuntu_pass = request.POST.get('ubuntu_pass')
    comment_1 = request.POST.get('comment_1')
    comment_2 = request.POST.get('comment_2')
    comment_3 = request.POST.get('comment_3')
    comment_4 = request.POST.get('comment_4')


    if not ssh_port:
        ssh_port = 22

    if _id =='':
        orm = table(IDC=IDC,position=position,application=application,external_IP=external_IP,ssh_port=ssh_port,
                    inner_IP_1=inner_IP_1,inner_IP_2=inner_IP_2,manage_IP=manage_IP,root_pass=root_pass,
                    ubuntu_pass=ubuntu_pass,comment_1=comment_1,comment_2=comment_2,comment_3=comment_3,
                    comment_4=comment_4)
    else:
        orm = table.objects.get(id=int(_id))
        orm.IDC = IDC
        orm.position = position
        orm.application = application
        orm.external_IP = external_IP
        orm.ssh_port = ssh_port
        orm.inner_IP_1 = inner_IP_1
        orm.inner_IP_2 = inner_IP_2
        orm.manage_IP = manage_IP
        orm.root_pass = root_pass
        orm.ubuntu_pass = ubuntu_pass
        orm.comment_1 = comment_1
        orm.comment_2 = comment_2
        orm.comment_3 = comment_3
        orm.comment_4 = comment_4
    try:
        orm.save()
        return HttpResponse(json.dumps({'code':0,'msg':u'保存成功'}),content_type="application/json")
    except Exception as e:
        # logger.error(e)
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")




@login_required
def server_info_del(request):
    _id = request.POST.get('id')
    orm = table.objects.get(id=_id)

    try:
        orm.delete()
        return HttpResponse(json.dumps({'code':0,'msg':u'删除成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")



# 服务器信息表(新)
@login_required
def server_info_table_new(request):
    # if not request.user.has_perm('server_info.can_view'):
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'server_info/server_info_table_new.html',{'user':request.user.username,
                                                               'path1':'server_info',
                                                               'path2':path,
                                                               'page_name1':u'信息表',
                                                               'page_name2':u'服务器信息表(新)'})



@login_required
def server_table_data(request):
    orm = server_table.objects.all()
    tableData = []
    for i in orm:
        tableData.append({
            'id': i.id,
            'class_1': i.class_1,
            'class_2': i.class_2,
            'class_3': i.class_3,
            'login_ip': i.login_ip,
            'ssh_port': i.ssh_port,
            'external_IP': i.external_IP,
            'inner_ip_1': i.inner_ip_1,
            'inner_ip_2': i.inner_ip_2,
            'root_password': i.root_password,
            'ubuntu_password': i.ubuntu_password,
            'db_password': i.db_password,
            'description': i.description,
            'manage_ip': i.manage_ip,
            'server_id': i.server_id,
            'comment_1': i.comment_1,
            'comment_2': i.comment_2,
            'IDC': i.IDC,
            'position': i.position,
            'owner': i.owner
        })
    return HttpResponse(json.dumps({'code':-1,'tableData':tableData}),content_type="application/json")



@login_required
def server_table_save(request):
    data = json.loads(request.body)
    _id = data.get('id')
    class_1 = data.get('class_1')
    class_2 = data.get('class_2')
    class_3 = data.get('class_3')
    login_ip = data.get('login_ip')
    ssh_port = data.get('ssh_port')
    external_IP = data.get('external_IP')
    inner_IP_1 = data.get('inner_IP_1')
    inner_IP_2 = data.get('inner_IP_2')
    root_password = data.get('root_password')
    ubuntu_password = data.get('ubuntu_password')
    db_password = data.get('db_password')
    description = data.get('description')
    manage_ip = data.get('manage_ip')
    server_id = data.get('server_id')
    comment_1 = data.get('comment_1')
    comment_2 = data.get('comment_2')
    IDC = data.get('IDC')
    position = data.get('position')
    owner = data.get('owner')

    if not ssh_port:
        ssh_port = 22

    orm = server_table.objects.get(id=int(_id))
    orm.class_1 = class_1
    orm.class_2 = class_2
    orm.class_3 = class_3
    orm.login_ip = login_ip
    orm.ssh_port = ssh_port
    orm.external_IP = external_IP
    orm.inner_IP_1 = inner_IP_1
    orm.inner_IP_2 = inner_IP_2
    orm.root_password = root_password
    orm.db_password = db_password
    orm.ubuntu_password = ubuntu_password
    orm.description = description
    orm.manage_ip = manage_ip
    orm.server_id = server_id
    orm.comment_1 = comment_1
    orm.comment_2 = comment_2
    orm.IDC = IDC
    orm.position = position
    orm.owner = owner

    try:
        orm.save()
        return HttpResponse(json.dumps({'code':0,'msg':u'保存成功'}),content_type="application/json")
    except Exception as e:
        # logger.error(e)
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")



@login_required
def domain_name_CRT_table(request):
    # if not request.user.has_perm('server_info.can_view'):
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'server_info/domain_name_CRT_table.html',{'user':request.user.username,
                                                               'path1':'server_info',
                                                               'path2':path,
                                                               'page_name1':u'信息表',
                                                               'page_name2':u'域名及证书信息表'})






@login_required
def domain_name_CRT_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    IDC = request.POST.get('IDC')

    aaData = []
    sort = ['name_server','apply_time','name_server_expiration_time','CRT_expiration_time','DNSPOD','account','comment','ICP']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = domain_name_CRT.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = domain_name_CRT.objects.all().count()
        else:
            result_data = domain_name_CRT.objects.filter(Q(IDC__contains=sSearch) | \
                                               Q(application__contains=sSearch) | \
                                               Q(external_IP__contains=sSearch) | \
                                               Q(inner_IP_1__contains=sSearch) | \
                                               Q(inner_IP_2__contains=sSearch) | \
                                               Q(manage_IP__contains=sSearch) | \
                                               Q(comment_1__contains=sSearch) | \
                                               Q(comment_2__contains=sSearch) | \
                                               Q(comment_3__contains=sSearch) | \
                                               Q(comment_4__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = domain_name_CRT.objects.filter(Q(IDC__contains=sSearch) | \
                                               Q(application__contains=sSearch) | \
                                               Q(external_IP__contains=sSearch) | \
                                               Q(inner_IP_1__contains=sSearch) | \
                                               Q(inner_IP_2__contains=sSearch) | \
                                               Q(manage_IP__contains=sSearch) | \
                                               Q(comment_1__contains=sSearch) | \
                                               Q(comment_2__contains=sSearch) | \
                                               Q(comment_3__contains=sSearch) | \
                                               Q(comment_4__contains=sSearch) | \
                                               Q(id__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = domain_name_CRT.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = domain_name_CRT.objects.all().count()
        else:
            result_data = domain_name_CRT.objects.filter(Q(IDC__contains=sSearch) | \
                                               Q(application__contains=sSearch) | \
                                               Q(external_IP__contains=sSearch) | \
                                               Q(inner_IP_1__contains=sSearch) | \
                                               Q(inner_IP_2__contains=sSearch) | \
                                               Q(manage_IP__contains=sSearch) | \
                                               Q(comment_1__contains=sSearch) | \
                                               Q(comment_2__contains=sSearch) | \
                                               Q(comment_3__contains=sSearch) | \
                                               Q(comment_4__contains=sSearch) | \
                                               Q(id__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = domain_name_CRT.objects.filter(Q(IDC__contains=sSearch) | \
                                               Q(application__contains=sSearch) | \
                                               Q(external_IP__contains=sSearch) | \
                                               Q(inner_IP_1__contains=sSearch) | \
                                               Q(inner_IP_2__contains=sSearch) | \
                                               Q(manage_IP__contains=sSearch) | \
                                               Q(comment_1__contains=sSearch) | \
                                               Q(comment_2__contains=sSearch) | \
                                               Q(comment_3__contains=sSearch) | \
                                               Q(comment_4__contains=sSearch) | \
                                               Q(id__contains=sSearch)).count()


    for i in  result_data:
        if i.apply_time == None:
            apply_time = ''
        else:
            apply_time = str(i.apply_time)

        if i.name_server_expiration_time == None:
            name_server_expiration_time = ''
        else:
            name_server_expiration_time = str(i.name_server_expiration_time)

        if i.CRT_expiration_time == None:
            CRT_expiration_time = ''
        else:
            CRT_expiration_time = str(i.CRT_expiration_time)
        aaData.append({
                       '0':i.name_server,
                       '1':apply_time,
                       '2':name_server_expiration_time,
                       '3':CRT_expiration_time,
                       '4':i.DNSPOD,
                       '5':i.account,
                       '6':i.comment,
                       '7':i.ICP,
                       '8':i.id,
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")





