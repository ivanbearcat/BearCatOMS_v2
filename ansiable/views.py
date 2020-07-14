#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json
from commons.ssh_commons import ssh_exec
from ansiable.apps import ansiable_host, ansiable_port
from ast import literal_eval
import subprocess
from dwebsocket import require_websocket
import time
import os
from ansiable.models import logs
from threading import Thread
import re


@login_required
def ansiable_playbook(request):
    path = request.path.split('/')[1]
    return render(request, 'ansiable/ansiable_playbook.html', {'user':request.user.username,
                                                     'path1':'ansiable',
                                                     'path2':path,
                                                     'page_name1':u'ansiable',
                                                     'page_name2':'ansiable-playbook'})


@login_required
def ansiable_playbook_data(request):
    result = literal_eval(ssh_exec(ansiable_host, ansiable_port ,'python /tmp/list.py'))
    return HttpResponse(json.dumps({'code': -1, 'tableData': result}), content_type='application/json;charset = utf-8')


@require_websocket
def ansiable_playbook_run(request):
    message = request.websocket.wait()
    message = json.loads(message)
    # 接收keepalive
    def keepalive_t(request):
        while 1:
            try:
                request.websocket.wait()
            except Exception:
                break
    Thread(target=keepalive_t, args=(request,)).start()
    playbook_path = message.get('playbook_path')
    # playbook_path = '/root/playbooks/xiaohulu/test.yaml'
    project_name = message.get('project_name')
    _type = message.get('type')

    if not (playbook_path and project_name and _type):
        request.websocket.send(json.dumps('error'))
    else:
        # 记录日志
        if _type == 1:
            operation = f'运行剧本 {playbook_path}'
        elif _type == 2:
            operation = f'运行剧本 [仅配置] {playbook_path}'
        orm_log = logs(name=request.user.username,
                       project_name=project_name,
                       operation=operation)
        orm_log.save()

        if _type == 1:
            p = subprocess.Popen(f'ssh {ansiable_host} -p {ansiable_port} "/usr/bin/ansible-playbook {playbook_path}"',
                                 shell=True, stdout=subprocess.PIPE)
        elif _type == 2:
            p = subprocess.Popen(f'ssh {ansiable_host} -p {ansiable_port} "/usr/bin/ansible-playbook {playbook_path} -t copyfile"',
                                 shell=True, stdout=subprocess.PIPE)
        while p.poll() == None:
            line = p.stdout.readline().decode()
            if line:
                request.websocket.send(json.dumps(line))




@login_required
def ansiable_playbook_config_edit(request):
    data = json.loads(request.body)
    project_name = data.get('project_name')
    config_file = data.get('config_file')
    config_data = data.get('config_data')
    backup_file = os.path.join(os.path.dirname(config_file), '.' + os.path.basename(config_file))
    if config_data:
        # config_data = config_data.replace('"', '\\"').replace("'", "\\'")
        # config_data = config_data.replace('"', '\\"').replace("'", "\\'").replace('$', '\\$')
        with open('/tmp/tmpfile', 'w') as f:
            f.write(config_data)
        p = subprocess.Popen(f'''
                    ssh {ansiable_host} -p {ansiable_port} "unalias cp; cp -a {config_file} {backup_file}"''', shell=True, stdout=subprocess.PIPE)
        while p.poll() != None:
            time.sleep(0.1)
        p = subprocess.Popen(f'''
                    scp -P {ansiable_port} /tmp/tmpfile {ansiable_host}:{config_file}
                ''', shell=True, stdout=subprocess.PIPE)
        while p.poll() != None:
            time.sleep(0.1)
        # 记录日志
        p = subprocess.Popen(f'ssh {ansiable_host} -p {ansiable_port} "/usr/bin/diff {config_file} {backup_file}"',
                             shell=True, stdout=subprocess.PIPE)
        while p.poll() != None:
            time.sleep(0.1)
        diff_result = p.stdout.read().decode().strip()
        operation = f'修改配置文件 {config_file} 修改内容 [diff]: {diff_result}'
        orm_log = logs(name=request.user.username,
                       project_name=project_name,
                       operation=operation)
        orm_log.save()

        return HttpResponse(json.dumps({'code': 0, 'msg': '编辑成功'}), content_type='application/json;charset = utf-8')
    else:
        p = subprocess.Popen(f'ssh {ansiable_host} -p {ansiable_port} "/usr/bin/cat {config_file}"',
                             shell=True, stdout=subprocess.PIPE)
        while p.poll() != None:
            time.sleep(0.1)
        result = p.stdout.read().decode().strip()
        code = p.returncode
        if code:
            return HttpResponse(json.dumps({'code': 1, 'msg': f'code: {code} 文件不存在或无法打开'}),
                                content_type='application/json;charset = utf-8')
        return HttpResponse(json.dumps({'code': -2, 'result': result}), content_type='application/json;charset = utf-8')



@login_required
def ansiable_playbook_change_branch(request):
    data = json.loads(request.body)
    project_name = data.get('project_name')
    vars_files = data.get('vars_files')
    branch_now = data.get('branch_now')
    change_branch = data.get('change_branch')

    # 记录日志
    operation = f'修改分支 {branch_now} -> {change_branch}'
    orm_log = logs(name=request.user.username,
                   project_name=project_name,
                   operation=operation)
    orm_log.save()

    print(f'''
        ssh {ansiable_host} -p {ansiable_port} "sed -i 's#branch: {branch_now}#branch: {change_branch}#' {vars_files}"
    ''')

    p = subprocess.Popen(f'''
        ssh {ansiable_host} -p {ansiable_port} "sed -i 's#branch: {branch_now}#branch: {change_branch}#' {vars_files}"
    ''',shell=True, stdout=subprocess.PIPE)
    while p.poll() != None:
        time.sleep(0.1)
    p.communicate()
    code = p.returncode
    if code:
        return HttpResponse(json.dumps({'code': 1, 'msg': f'code: {code} 文件不存在或执行出错'}),
                            content_type='application/json;charset = utf-8')
    return HttpResponse(json.dumps({'code': 0, 'msg': '修改成功'}), content_type='application/json;charset = utf-8')


@login_required
def ansiable_playbook_log(request):
    path = request.path.split('/')[1]
    return render(request, 'ansiable/ansiable_playbook_log.html', {'user':request.user.username,
                                                     'path1':'ansiable',
                                                     'path2':path,
                                                     'page_name1':u'ansiable',
                                                     'page_name2':'操作日志'})


@login_required
def ansiable_playbook_log_data(request):
    orm = logs.objects.all()
    tableData = []
    for i in orm:
        tableData.append({
            'name': i.name,
            'project_name': i.project_name,
            'operation': i.operation,
            'time': str(i.time).split('.')[0]
        })
    return HttpResponse(json.dumps({'code': -1, 'tableData': tableData}), content_type="application/json")



@login_required
def upload(request):
    # 接收文件
    file = request.FILES.get('image', None)
    backup = request.POST.get('backup', None)
    update = request.POST.get('update', None)
    filename = re.sub(r'\(\d+\)', '', file.name)

    with open(f'/tmp/{filename}', 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)

    result = literal_eval(ssh_exec(ansiable_host, ansiable_port, 'python /tmp/list.py'))

    log = ''
    for i in result:
        if i['project_name'] == filename.split('.')[0]:
            # 判断文件名是否在已存在项目中
            playbook_path = i['playbook_path']
            # 复制文件到ansible机器
            remote_jar_dir = '/work/jars/'
            if backup != None and backup == 'true':
                # 备份远程jar包
                p0 = subprocess.Popen(f'ssh {ansiable_host} -p {ansiable_port} "\mv {remote_jar_dir}{filename}{{,_bak}}"',
                                  shell=True, stdout=subprocess.PIPE)
                p0.wait()
            # 上传jar包
            p1 = subprocess.Popen(f'scp -P {ansiable_port} /tmp/{filename} {ansiable_host}:{remote_jar_dir}',
                                 shell=True, stdout=subprocess.PIPE)
            p1.wait()
            if update != None and update == 'true':
                # 运行ansible-playbook
                p2 = subprocess.Popen(f'ssh {ansiable_host} -p {ansiable_port} "/usr/bin/ansible-playbook {playbook_path}"',
                                     shell=True, stdout=subprocess.PIPE)
                p2.wait()
                p_resutl = p2.stdout.read().decode()
                if p_resutl:
                    log = p_resutl
            break
    else:
        return HttpResponse(json.dumps({'code': 1, 'msg': '没有查到改项目无法更新'}), content_type="application/json")
    return HttpResponse(json.dumps({'code': 0, 'msg': '成功', 'log': log}), content_type="application/json")



@login_required
def quick_update(request):
    path = request.path.split('/')[1]
    return render(request, 'ansiable/quick_update.html', {'user': request.user.username,
                                                               'path1': 'ansiable',
                                                               'path2': path,
                                                               'page_name1': u'ansiable',
                                                               'page_name2': '快速更新'})




