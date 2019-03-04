# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from BearCatOMSv2.settings import logger
from django.contrib.auth.decorators import login_required
import json
from django.db.models.query_utils import Q
from operation.models import server_list,command_template
from server_info.models import table
from commons.ssh_test import test
from threading import Thread
from queue import Queue
import paramiko
from  concurrent.futures import ThreadPoolExecutor
import subprocess
import pexpect


# from audit.models import log
# from libs.socket_send_data import client_send_data
# from libs.check_center_server import check_center_server_up



@login_required
def cmd_template(request):
    # flag = check_permission(u'命令模板',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'operation/cmd_template.html',{'user':request.user.username,
                                                           'path1':'operation',
                                                           'path2':path,
                                                           'page_name1':u'运维操作',
                                                           'page_name2':u'命令模板'})

def cmd_template_data(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['description','cmd']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = command_template.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = command_template.objects.all().count()
        else:
            result_data = command_template.objects.filter(Q(description__contains=sSearch) | \
                                               Q(cmd__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = command_template.objects.filter(Q(description__contains=sSearch) | \
                                                 Q(cmd__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = command_template.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = command_template.objects.all().count()
        else:
            result_data = command_template.objects.filter(Q(description__contains=sSearch) | \
                                               Q(cmd__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = command_template.objects.filter(Q(description__contains=sSearch) | \
                                                 Q(cmd__contains=sSearch)).count()

    for i in result_data:
        cmd_list = []
        cmd = i.cmd.replace('<','&lt;').replace('>','&gt;')
        for j in cmd.split('\n'):
            cmd_list.append(j+'<br>')
        aaData.append({
                       '0': i.description,
                       '1':''.join(cmd_list),
                       '2': i.id
                      })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")




@login_required
def cmd_template_save(request):
    _id = request.POST.get('id')
    description = request.POST.get('description')
    cmd = request.POST.get('cmd')

    try:
        if _id =='':
            command_template.objects.create(description=description,cmd=cmd)
        else:
            orm = command_template.objects.get(id=_id)
            orm.description = description
            orm.cmd = cmd
            orm.save()
        return HttpResponse(json.dumps({'code':0,'msg':u'保存成功'}),content_type="application/json")
    except Exception as e:
        logger.error(e)
        return HttpResponse(json.dumps({'code':1,'msg':str(e)}),content_type="application/json")




@login_required
def cmd_template_dropdown(request):
    result = []
    orm = command_template.objects.all()
    for i in orm:
        result.append({'text':i.description,'id':i.id})
    return HttpResponse(json.dumps(result),content_type="application/json")




@login_required
def cmd_template_del(request):
    try:
        _id = request.POST.get('id')
        orm = command_template.objects.get(id=_id)
        orm.delete()
        return HttpResponse(json.dumps({'code':0,'msg':u'删除成功'}),content_type="application/json")
    except Exception as e:
        logger.error(e)
        return HttpResponse(json.dumps({'code':1,'msg':u'删除失败'}),content_type="application/json")



@login_required
def server_operation(request):
    # flag = check_permission(u'服务器操作',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request,'operation/server_operation.html',{'user':request.user.username,
                                                           'path1':'operation',
                                                           'path2':path,
                                                           'page_name1':u'运维操作',
                                                           'page_name2':u'服务器操作'})


@login_required
def get_server_list(request):
    sEcho =  request.POST.get('sEcho') #标志，直接返回
    iDisplayStart = int(request.POST.get('iDisplayStart'))#第几行开始
    iDisplayLength = int(request.POST.get('iDisplayLength'))#显示多少行
    iSortCol_0 = int(request.POST.get("iSortCol_0"))#排序行号
    sSortDir_0 = request.POST.get('sSortDir_0')#asc/desc
    sSearch = request.POST.get('sSearch')#高级搜索

    aaData = []
    sort = ['server_name','external_ip','ssh_port','os']

    if  sSortDir_0 == 'asc':
        if sSearch == '':
            result_data = server_list.objects.all().order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = server_list.objects.all().count()
        else:
            result_data = server_list.objects.filter(Q(server_name__contains=sSearch) | \
                                               Q(external_ip__contains=sSearch) | \
                                               Q(os__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0])[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = server_list.objects.filter(Q(server_name__contains=sSearch) | \
                                                 Q(external_ip__contains=sSearch) | \
                                                 Q(os__contains=sSearch)).count()
    else:
        if sSearch == '':
            result_data = server_list.objects.all().order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = server_list.objects.all().count()
        else:
            result_data = server_list.objects.filter(Q(server_name__contains=sSearch) | \
                                               Q(external_ip__contains=sSearch) | \
                                               Q(os__contains=sSearch)) \
                                            .order_by(sort[iSortCol_0]).reverse()[iDisplayStart:iDisplayStart+iDisplayLength]
            iTotalRecords = server_list.objects.filter(Q(server_name__contains=sSearch) | \
                                                 Q(external_ip__contains=sSearch) | \
                                                 Q(os__contains=sSearch)).count()



    for i in  result_data:
            aaData.append({
                           '0':i.server_name,
                           '1':i.external_ip,
                           '2':i.ssh_port,
                           '3':i.os,
                           '4':i.root_pass,
                           '5':i.id
                          })
    result = {'sEcho':sEcho,
               'iTotalRecords':iTotalRecords,
               'iTotalDisplayRecords':iTotalRecords,
               'aaData':aaData
    }
    return HttpResponse(json.dumps(result),content_type="application/json")




def ssh_test(hostname, username, password, port, server_name):
    try:
        ssh=paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password, port=port, timeout=2)
        ssh.close()
        # print('secuess')
        # q.put((hostname, password))
        return (hostname, password, port, server_name)
    except Exception as e:
        # print(f'fail: {e}')
        pass

def ssh_copy_id(hostname, password, port=22):
    child=pexpect.spawn(f'ssh-copy-id {hostname} > /dev/null 2>&1')
    child.expect ('password:')
    child.sendline(password)
    child.expect('$')
    child.interact()
    child.close()

@login_required
def search_server_list(request):
    server_info_orm = table.objects.all()
    server_passwd_list = []
    for server_info in server_info_orm:
        server_name = server_info.application
        external_IP = server_info.external_IP
        root_pass = server_info.root_pass
        ssh_port = server_info.ssh_port
        if not ssh_port:
            ssh_port = 22

        if external_IP != '' and root_pass != '':
            server_passwd_list.append([external_IP, root_pass, ssh_port, server_name])

    p = ThreadPoolExecutor(20)
    thread_list = []
    for server_passwd in server_passwd_list:
        thread_list.append(p.submit(ssh_test,server_passwd[0], 'root', server_passwd[1], server_passwd[2], server_passwd[3]))

    p.shutdown()

    sucess_server_passwd_list = []
    for thread in thread_list:
        thread_result = thread.result()
        if thread_result:
            sucess_server_passwd_list.append(thread_result)

    insert_list = []
    for sucess_server_passwd in sucess_server_passwd_list:
        print(sucess_server_passwd)
        insert_list.append(server_list(server_name=sucess_server_passwd[3].replace(' ','_'), external_ip=sucess_server_passwd[0],
                                       root_pass=sucess_server_passwd[1], ssh_port=sucess_server_passwd[2],
                                       os='linux'))
    server_list.objects.all().delete()
    server_list.objects.bulk_create(insert_list)

    # with open('/etc/salt/roster', 'w') as f:
    #     for sucess_server_passwd in sucess_server_passwd_list:
    #         data = f'{sucess_server_passwd[3]}:\n    host: {sucess_server_passwd[0]}\n    user: root\n    passwd: {sucess_server_passwd[1]}\n    port: {sucess_server_passwd[2]}\n\n'
    #         f.write(data)
    # subprocess.Popen('salt-ssh "*" -i test.ping', shell=True)
    with open('/etc/ansible/hosts', 'w') as f:
        for sucess_server_passwd in sucess_server_passwd_list:
            data = f"[{sucess_server_passwd[3].replace(' ','_')}]\n{sucess_server_passwd[0]}\n\n"
            f.write(data)

    p = ThreadPoolExecutor(20)
    orm = server_list.objects.all()
    for i in orm:
        print(f'ssh_copy_id {i.external_ip} {i.root_pass}')
        p.submit(ssh_copy_id, i.external_ip, i.root_pass)
    p.shutdown()

    return HttpResponse(json.dumps({'code':0,'msg':u'获取完成'}),content_type="application/json")



@login_required
def run_cmd(request):
    try:
        server_names = request.POST.get('server_names')
        belong_tos = request.POST.get('belong_tos')
        server_names = server_names.split(',')
        belong_tos = belong_tos.split(',')
        cmd = request.POST.get('cmd')
        cmd_template = request.POST.get('cmd_template')


        # for i in server_names:
        #     log.objects.create(source_ip=i,username=request.user.username,command=cmd,time=time_now)
        return HttpResponse(json.dumps({'code':0,'msg':u'完成执行完成','cmd_results':cmd_results}),content_type="application/json")
    except Exception as e:
        logger.error(e)
        return HttpResponse(json.dumps({'code':1,'msg':u'完成执行失败'}),content_type="application/json")




