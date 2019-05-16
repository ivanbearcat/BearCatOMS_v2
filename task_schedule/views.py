# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from task_schedule.models import tasks
import json
import subprocess
import time
import datetime
import threading
import os
import signal
from dwebsocket import require_websocket
import re
from task_schedule.apps import type_dict
from commons.socket_send_data import tunnel_send




@require_websocket
def log_web_socket(request):
    message = request.websocket.wait()
    message = json.loads(message)

    orm = tasks.objects.get(id=message['id'])
    host = orm.target.split(':')[0]
    port = orm.target.split(':')[1]


    while 1:
        try:
            request.websocket.read()
        except EOFError:
            break
        if message['pods_name'] != '':
            p = subprocess.Popen(f"ssh {host} -p {port} 'kubectl logs {message['pods_name']}'", shell=True, stdout=subprocess.PIPE)
        else:
            p = subprocess.Popen(f'''ssh {host} -p {port} "cat /tmp/{message['name']}.log"''', shell=True,
                                 stdout=subprocess.PIPE)
        p.wait()
        stdout = p.stdout.read().decode()
        if stdout:
            request.websocket.send(json.dumps(stdout))
        time.sleep(0.5)

    # else:
    #
    #     stdout = p.stdout.read().decode().strip()
    #     if stdout:
    #         request.websocket.send(json.dumps(stdout))
    #         while 1:
    #             try:
    #                 request.websocket.read()
    #             except EOFError:
    #                 break
    #
    #             stdout = p.stdout.readline().decode().strip()
    #             if stdout:
    #                 request.websocket.send(json.dumps(stdout))
    #             time.sleep(0.1)
    #     else:
    #         request.websocket.send('日志还未生成，稍后再试')


@login_required
def task_table(request):
    # flag = check_permission(u'nagios',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request, 'task_schedule/task_schedule_single.html', {'user':request.user.username,
                                                     'path1':'task_schedule',
                                                     'path2':path,
                                                     'page_name1':u'任务调度',
                                                     'page_name2':'任务'})

@login_required
def task_table_data(request):
    orm = tasks.objects.all()
    tableData = []
    for i in orm:
        tableData.append({
            'id': i.id,
            'task_name': i.task_name,
            'task_desc': i.task_desc,
            'task_type': i.task_type,
            'target': i.target,
            'task_cmd': i.task_cmd,
            'duration': i.duration.split('.')[0],
            'status': i.status,
            'pods_name': i.pods_name,
            'create_time': str(i.create_time).split('.')[0],
            'last_run_time': str(i.last_run_time).split('.')[0]
        })
    # 探测任务是否结束
    try:
        orm_sub = tasks.objects.filter(status='运行中')
        for i in orm_sub:
            host = i.target.split(':')[0]
            port = i.target.split(':')[1]
            p = subprocess.Popen(f'ssh {host} -p {port} "tail -1 /tmp/{i.task_name}.log"', shell=True, stdout=subprocess.PIPE)
            p.wait()
            stdout, stderr = p.communicate()
            stdout_list = stdout.decode().strip().split()
            if  len(stdout_list) == 3 and stdout_list[0] == 'done':
                if stdout_list[1] == '0':
                    i.status = '已完成'
                elif stdout_list[1] == '-9':
                    i.status = '已终止'
                else:
                    i.status = '执行错误'
                i.duration = stdout_list[2]
                i.save()
    except Exception as e:
        print(e)
    return HttpResponse(json.dumps({'code':-1,'tableData':tableData}),content_type="application/json")

@login_required
def task_table_save(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        task_name = data.get('task_name')
        task_desc = data.get('task_desc')
        task_type = data.get('task_type')
        target = data.get('target')
        task_cmd = data.get('task_cmd')
        if not _id:
            orm = tasks(task_name=task_name, task_desc=task_desc, task_type=task_type, target=target, task_cmd=task_cmd,
                        status='未执行', pods_name='')
        else:
            orm = tasks.objects.get(id=_id)
            orm.task_name = task_name
            orm.task_desc = task_desc
            orm.task_type = task_type
            orm.target = target
            orm.task_cmd = task_cmd
        orm.save()
        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")

@login_required
def task_table_del(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        orm = tasks.objects.get(id=_id)
        orm.delete()
        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")

# @login_required
# def task_table_run(request):
#     try:
#         data = json.loads(request.body)
#         _id = data.get('id')
#         orm = tasks.objects.get(id=_id)
#         name = orm.task_name
#         _type = orm.task_type
#
#         host = orm.target.split(':')[0]
#         port = orm.target.split(':')[1]
#         cmd = orm.task_cmd
#         status = orm.status
#         if status == '运行中':
#             return HttpResponse(json.dumps({'code': 1, 'msg': '任务正在执行'}), content_type="application/json")
#         tmp_file = f'/tmp/{name}{type_dict[_type]["suffix"]}'
#         with open(tmp_file, 'w') as f:
#             f.write(cmd)
#         start_time = time.time()
#
#         if os.path.exists(f'/tmp/{name}.log'):
#             os.remove(f'/tmp/{name}.log')
#         p = subprocess.Popen(f'''
#                 scp -P {port} {tmp_file} {host}:/tmp > /dev/null 2>&1
#                 ssh {host} -p {port} '{type_dict[_type]["bin"]} {tmp_file}' > /tmp/{name}.log 2>&1
#             ''', shell=True)
#         orm.last_run_time = str(datetime.datetime.now())
#         orm.pid = p.pid
#         orm.status = '运行中'
#         orm.save()
#
#         def k8s_call_back(orm, name):
#             count = 0
#             while 1:
#                 p = subprocess.Popen(
#                     f"grep Running /tmp/{name}.log" + f" > /dev/null 2>&1 && grep 'pod name' /tmp/{name}.log" + "|uniq|awk -F':' '{print $2}'",
#                     shell=True, stdout=subprocess.PIPE)
#                 p.wait()
#                 stdout, stderr = p.communicate()
#                 if stdout:
#                     pods_name = stdout.decode().strip()
#                     orm.pods_name = pods_name
#                     orm.save()
#                     break
#                 else:
#                     if count == 30:
#                         break
#                     time.sleep(1)
#                     count += 1
#                     continue
#
#         def status_call_back(orm, p):
#             code = p.wait()
#             if code == 0:
#                 orm.status = '已完成'
#             elif code == -9:
#                 orm.status = '已终止'
#             else:
#                 orm.status = '执行错误'
#             stop_time = time.time()
#             orm.duration = str(stop_time - start_time)
#             orm.pid = ''
#             orm.save()
#
#         threading.Thread(target=status_call_back, args=(orm, p)).start()
#         if _type == 'k8s-shell':
#             threading.Thread(target=k8s_call_back, args=(orm, name)).start()
#
#         return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
#     except Exception as e:
#         orm.status = '执行错误'
#         orm.save()
#         return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")

@login_required
def task_table_run(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        orm = tasks.objects.get(id=_id)
        name = orm.task_name
        _type = orm.task_type

        host = orm.target.split(':')[0]
        port = int(orm.target.split(':')[1])
        cmd = orm.task_cmd
        status = orm.status
        if status == '运行中':
            return HttpResponse(json.dumps({'code': 1, 'msg': '任务正在执行'}), content_type="application/json")
        # 调用socket接口启动脚本
        data = {
            'name': name,
            'cmd': cmd,
            'suffix': type_dict[_type]["suffix"],
            'bin': type_dict[_type]["bin"]
        }
        code = tunnel_send(host, port, data)
        if code == 0:
            orm.last_run_time = str(datetime.datetime.now())
            orm.status = '运行中'
            orm.save()

        def k8s_call_back(orm, name, host, port):
            # 从远程机器的shell日志判断Running状态，并获取pods名入库
            count = 0
            while 1:
                p = subprocess.Popen(
                    f'ssh {host} -p {port} "grep Running /tmp/{name}.log' +
                    f" > /dev/null 2>&1 && grep 'pod name' /tmp/{name}.log" +
                    '''|uniq"|awk -F':' '{print $2}' ''',
                    shell=True, stdout=subprocess.PIPE)
                p.wait()
                stdout, stderr = p.communicate()
                if stdout:
                    pods_name = stdout.decode().strip()
                    orm.pods_name = pods_name
                    orm.save()
                    break
                else:
                    if count == 30:
                        break
                    time.sleep(1)
                    count += 1
                    continue

        if _type == 'k8s-shell':
            threading.Thread(target=k8s_call_back, args=(orm, name, host, port)).start()

        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        orm.status = '执行错误'
        orm.save()
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")

@login_required
def task_table_kill(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        orm = tasks.objects.get(id=_id)
        name = orm.task_name
        _type = orm.task_type

        host = orm.target.split(':')[0]
        port = orm.target.split(':')[1]
        tmp_file = f'/tmp/{name}{type_dict[_type]["suffix"]}'
        p = subprocess.Popen(f'ssh {host} -p {port} "ps aux|grep {tmp_file}' + '''|grep -v grep"|awk '{print $2}' ''', shell=True, stdout=subprocess.PIPE)
        p.wait()
        stdout,stderr = p.communicate()
        if stdout:
            pids = ' '.join(stdout.decode().strip().split('\n'))
            subprocess.call(f'ssh {host} -p {port} "kill -9 {pids}"', shell=True)
        else:
            orm.status = '已终止'
            orm.save()
        if orm.task_type == 'k8s-shell':
            orm.pods_name = ''
            orm.save()
            task_name = re.search(r'--name (.*?) ', orm.task_cmd).group(1)
            def thread_run():
                p = subprocess.Popen(f"ssh {host} -p {port} kubectl get pods |grep {task_name}" + "|grep driver|awk '{print $1}'",
                                     shell=True, stdout=subprocess.PIPE)
                p.wait()
                stdout, stderr = p.communicate()
                if stdout:
                    for i in stdout.decode().strip().split('\n'):
                        subprocess.call(f'ssh {host} -p {port} "kubectl delete pods {i}"', shell=True)
            threading.Thread(target=thread_run).start()

        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")