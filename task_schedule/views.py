# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from task_schedule.models import single_tasks, task_group
import json
import subprocess
import time
import threading
from dwebsocket import require_websocket
import re
from task_schedule.apps import type_dict,k8s_host, k8s_port, ssh_server
from task_schedule import tasks
from celery.task.control import revoke
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.db.models import Q
from BearCatOMSv2.settings import TIME_ZONE
from commons.ssh_commons import ssh_exec
from commons.timer import timer
from ast import literal_eval
from threading import Thread
import sys
import fcntl
import os


@require_websocket
def log_web_socket(request):
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

    orm = single_tasks.objects.get(id=message['id'])
    host = orm.target.split(':')[0]
    port = orm.target.split(':')[1]
    # 获取正在运行的pod名
    pods_name_Running = ''
    if message['pods_name'] != '':
        tmp_list = message['pods_name'].split('-')
        tmp_list[-2] = '.*'
        pods_name = '-'.join(tmp_list)

        pods_Running = subprocess.Popen(f'ssh {host} -p {port} "kubectl get pods -nspark-cluster |grep {pods_name}|grep Running"|' +
                                        "awk '{print $1}'", shell=True, stdout=subprocess.PIPE)
        print(f'ssh {host} -p {port} "kubectl get pods -nspark-cluster|grep {pods_name}|grep Running"|' +
                                        "awk '{print $1}'")
        pods_Running.wait()
        pods_name_Running = pods_Running.stdout.read().decode().strip()
        print(pods_name_Running)

    while 1:
        try:
            request.websocket.read()
        except EOFError:
            break
        if pods_name_Running != '':
            p = subprocess.Popen(f"ssh {host} -p {port} 'kubectl logs {pods_name_Running} -nspark-cluster'", shell=True, stdout=subprocess.PIPE)
            # p = subprocess.Popen(f'''ssh {host} -p {port} "cat {orm.k8s_log}"''', shell=True,
            #                      stdout=subprocess.PIPE)
        else:
            p = subprocess.Popen(f'''ssh {host} -p {port} "cat /tmp/{message['name']}.log"''', shell=True,
                                 stdout=subprocess.PIPE)
        while p.poll() != None:
            time.sleep(0.1)
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
    return render(request, 'task_schedule/task_single.html', {'user':request.user.username,
                                                     'path1':'task_schedule',
                                                     'path2':path,
                                                     'page_name1':u'任务调度',
                                                     'page_name2':'任务'})



@login_required
def task_table_data(request):
    orm = single_tasks.objects.all()
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
        orm_sub = single_tasks.objects.filter(status='运行中')
        for i in orm_sub:
            host = i.target.split(':')[0]
            port = i.target.split(':')[1]
            p = subprocess.Popen(f'ssh {host} -p {port} "tail -1 /tmp/{i.task_name}.log"', shell=True, stdout=subprocess.PIPE)
            while p.poll() != None:
                time.sleep(0.1)
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
            # 脚本如果没有设置重定向日志，则设置默认重定向日志
            # if task_type == 'k8s-shell':
            #     if ('>' or '>>') in re.search(r'\.jar.*(\n|$)',task_cmd).group():
            #         k8s_log = re.search(r'\.jar.*>+(.*)(\n|$)',task_cmd).group(1).strip()
            #     else:
            #         k8s_log = f'/tmp/{task_name}_k8s.log'
            #         task_cmd = re.sub(r'(\.jar.*)(\n|$)', f'\\1 >> {k8s_log}\n', task_cmd)
            orm = single_tasks(task_name=task_name, task_desc=task_desc, task_type=task_type, target=target, task_cmd=task_cmd,
                        status='未执行', pods_name='')
        else:
            orm = single_tasks.objects.get(id=_id)
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
        orm = single_tasks.objects.get(id=_id)
        orm.delete()
        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



# @login_required
# def task_table_run(request):
#     try:
#         data = json.loads(request.body)
#         _id = data.get('id')
#         orm = single_tasks.objects.get(id=_id)
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
        task_name = data.get('task_name')
        # orm = single_tasks.objects.get(id=_id)
        # name = orm.task_name
        # _type = orm.task_type
        #
        # host = orm.target.split(':')[0]
        # port = int(orm.target.split(':')[1])
        # cmd = orm.task_cmd
        # status = orm.status
        # if status == '运行中':
        #     return HttpResponse(json.dumps({'code': 1, 'msg': '任务正在执行'}), content_type="application/json")
        # # 调用socket接口启动脚本
        # data = {
        #     'name': name,
        #     'cmd': cmd,
        #     'suffix': type_dict[_type]["suffix"],
        #     'bin': type_dict[_type]["bin"]
        # }
        # code = tunnel_send(host, port, data)
        # if code == 0:
        #     orm.last_run_time = str(datetime.datetime.now())
        #     orm.status = '运行中'
        #     orm.save()
        #
        # def k8s_call_back(orm, name, host, port):
        #     # 从远程机器的shell日志判断Running状态，并获取pods名入库
        #     count = 0
        #     while 1:
        #         p = subprocess.Popen(
        #             f'ssh {host} -p {port} "grep Running /tmp/{name}.log' +
        #             f" > /dev/null 2>&1 && grep 'pod name' /tmp/{name}.log" +
        #             '''|uniq"|awk -F':' '{print $2}' ''',
        #             shell=True, stdout=subprocess.PIPE)
        #         p.wait()
        #         stdout, stderr = p.communicate()
        #         if stdout:
        #             pods_name = stdout.decode().strip()
        #             orm.pods_name = pods_name
        #             orm.save()
        #             break
        #         else:
        #             if count == 30:
        #                 break
        #             time.sleep(1)
        #             count += 1
        #             continue
        #
        # if _type == 'k8s-shell':
        #     threading.Thread(target=k8s_call_back, args=(orm, name, host, port)).start()
        tasks.run_task.delay(task_name)

        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_table_kill(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        orm = single_tasks.objects.get(id=_id)
        name = orm.task_name
        _type = orm.task_type
        task_id = orm.task_id

        revoke(task_id, terminate=True)
        host = orm.target.split(':')[0]
        port = orm.target.split(':')[1]
        tmp_file = f'/tmp/{name}{type_dict[_type]["suffix"]}'
        p = subprocess.Popen(f'ssh {host} -p {port} "ps aux|grep {tmp_file}' + '''|grep -v grep"|awk '{print $2}' ''', shell=True, stdout=subprocess.PIPE)
        while p.poll() != None:
            time.sleep(0.1)
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
            task_name = re.search(r'--name (.*?) ', orm.task_cmd).group(1).lower()
            def thread_run():
                p = subprocess.Popen(f"ssh {host} -p {port} kubectl get pods -nspark-cluster |grep {task_name}" + "|egrep '(driver)?'|egrep '(Running|Pending)'|awk '{print $1}'",
                                     shell=True, stdout=subprocess.PIPE)
                while p.poll() != None:
                    time.sleep(0.1)
                stdout, stderr = p.communicate()
                if stdout:
                    for i in stdout.decode().strip().split('\n'):
                        subprocess.call(f'ssh {host} -p {port} "kubectl delete pods {i} -nspark-cluster"', shell=True)
            threading.Thread(target=thread_run).start()

        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_table_group(request):
    # flag = check_permission(u'nagios',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request, 'task_schedule/task_group.html', {'user':request.user.username,
                                                     'path1':'task_schedule',
                                                     'path2':path,
                                                     'page_name1':u'任务调度',
                                                     'page_name2':'任务组'})



@login_required
def task_table_group_data(request):
    orm = task_group.objects.all()
    tableData = []
    for i in orm:
        try:
            group_content = literal_eval(i.group_content)
        except Exception:
            group_content =i.group_content
        tableData.append({
            'id': i.id,
            'group_name': i.group_name,
            'group_desc': i.group_desc,
            'group_content': group_content,
            'duration': i.duration.split('.')[0],
            'status': i.status,
            'task_now': i.task_now,
            'create_time': str(i.create_time).split('.')[0],
            'last_run_time': str(i.last_run_time).split('.')[0]
        })
    return HttpResponse(json.dumps({'code':-1,'tableData':tableData}),content_type="application/json")



@login_required
def task_table_group_save(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        group_name = data.get('group_name')
        group_desc = data.get('group_desc')
        group_content = data.get('group_content')
        if not _id:
            orm = task_group(group_name=group_name, group_desc=group_desc, group_content=group_content, status='未执行')
        else:
            orm = task_group.objects.get(id=_id)
            orm.group_name = group_name
            orm.group_desc = group_desc
            orm.group_content = group_content
        orm.save()
        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_table_group_del(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        orm = task_group.objects.get(id=_id)
        orm.delete()
        return HttpResponse(json.dumps({'code': 0, 'msg': '操作成功'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_table_group_run(request):
    try:
        data = json.loads(request.body)
        group_name = data.get('group_name')
        tasks.run_tasks.delay(group_name)

        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_table_group_kill(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        orm_group = task_group.objects.get(id=_id)
        task_now = orm_group.task_now
        task_id = orm_group.task_id
        orm = single_tasks.objects.get(task_name=task_now)
        name = orm.task_name
        _type = orm.task_type


        revoke(task_id, terminate=True)
        orm_group.status = '已终止'
        orm_group.save()

        host = orm.target.split(':')[0]
        port = orm.target.split(':')[1]
        tmp_file = f'/tmp/{name}{type_dict[_type]["suffix"]}'
        p = subprocess.Popen(f'ssh {host} -p {port} "ps aux|grep {tmp_file}' + '''|grep -v grep"|awk '{print $2}' ''', shell=True, stdout=subprocess.PIPE)
        while p.poll() != None:
            time.sleep(0.1)
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
            task_name = re.search(r'--name (.*?) ', orm.task_cmd).group(1).lower()
            def thread_run():
                p = subprocess.Popen(f"ssh {host} -p {port} kubectl get pods -nspark-cluster|grep {task_name}" + "|grep driver|grep Running|awk '{print $1}'",
                                     shell=True, stdout=subprocess.PIPE)
                while p.poll() != None:
                    time.sleep(0.1)
                stdout, stderr = p.communicate()
                if stdout:
                    for i in stdout.decode().strip().split('\n'):
                        subprocess.call(f'ssh {host} -p {port} "kubectl delete pods {i} -nspark-cluster"', shell=True)
            threading.Thread(target=thread_run).start()

        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_schedule_table(request):
    # flag = check_permission(u'nagios',request.user.username)
    # if flag < 1:
    #     return render(request,'public/no_passing.html')
    path = request.path.split('/')[1]
    return render(request, 'task_schedule/task_schedule.html', {'user':request.user.username,
                                                                 'path1':'task_schedule',
                                                                 'path2':path,
                                                                 'page_name1':u'任务调度',
                                                                 'page_name2':'计划任务'})



@login_required
def task_schedule_data(request):
    orm = PeriodicTask.objects.all()
    tableData = []
    for i in orm:
        if i.name == 'celery.backend_cleanup':
            continue
        if i.task == 'task_schedule.tasks.run_task':
            task_type = '单任务'
        elif i.task == 'task_schedule.tasks.run_tasks':
            task_type = '任务组'
        else:
            task_type = ''
        if not i.args == '[]':
            task_name = literal_eval(i.args)[0]
        else:
            task_name = ''
        orm_cron = CrontabSchedule.objects.get(id=i.crontab_id)
        crontab = f'{orm_cron.minute} {orm_cron.hour} {orm_cron.day_of_week} {orm_cron.day_of_month} {orm_cron.month_of_year}'
        # if i.enabled:
        #     enabled = '启用'
        # else:
        #     enabled = '关闭'
        tableData.append({
            'id': i.id,
            'name': i.name,
            'task_type': task_type,
            'task_name': task_name,
            'enabled': i.enabled,
            'last_run_at': str(i.last_run_at).split('.')[0],
            'crontab': crontab
        })
    return HttpResponse(json.dumps({'code':-1,'tableData':tableData}),content_type="application/json")



@login_required
def task_schedule_save(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        name = data.get('name')
        crontab = data.get('crontab')
        task_type = data.get('task_type')
        task_name = data.get('task_name')
        # 处理crontab表格式
        if len(crontab.strip().split()) != 5:
            return HttpResponse(json.dumps({'code': 1, 'msg': 'crontab格式错误'}), content_type="application/json")
        else:
            minute, hour, day_of_week, day_of_month, month_of_year = crontab.strip().split()
        orm_crontab = CrontabSchedule.objects.filter(Q(minute=minute) &
                                                     Q(hour=hour) &
                                                     Q(day_of_week=day_of_week) &
                                                     Q(day_of_month=day_of_month) &
                                                     Q(month_of_year=month_of_year))
        if orm_crontab:
            crontab_id = orm_crontab[0].id
        else:
            orm_crontab = CrontabSchedule(minute=minute,
                                          hour=hour,
                                          day_of_week=day_of_week,
                                          day_of_month=day_of_month,
                                          month_of_year=month_of_year,
                                          timezone=TIME_ZONE)
            orm_crontab.save()
            crontab_id = orm_crontab.id
        # 处理任务表格式
        if task_type == '单任务':
            task = 'task_schedule.tasks.run_task'
        elif task_type == '任务组':
            task = 'task_schedule.tasks.run_tasks'
        args = f'["{task_name}"]'
        # 添加和编辑
        if not _id:
            orm = PeriodicTask(name=name,
                         task=task,
                         args=args,
                         crontab_id=crontab_id)

        else:
            orm = PeriodicTask.objects.get(id=_id)
            orm.name = name
            orm.task = task
            orm.args = args
            orm.crontab_id = crontab_id
        orm.save()
        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_schedule_switch(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        enabled = data.get('enabled')
        orm = PeriodicTask.objects.get(id=_id)
        orm.enabled = enabled
        orm.save()
        return HttpResponse(json.dumps({'code': 0, 'msg': '操作成功'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_schedule_del(request):
    try:
        data = json.loads(request.body)
        _id = data.get('id')
        orm = PeriodicTask.objects.get(id=_id)
        orm_crontab = CrontabSchedule.objects.get(id=orm.crontab_id)
        orm_crontab.delete()
        orm.delete()
        return HttpResponse(json.dumps({'code': 0, 'msg': '操作成功'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_schedule_scripts(request):
    path = request.path.split('/')[1]
    return render(request, 'task_schedule/task_schedule_scripts.html', {'user':request.user.username,
                                                     'path1':'task_schedule',
                                                     'path2':path,
                                                     'page_name1':u'任务调度',
                                                     'page_name2':'脚本'})



@login_required
def task_schedule_scripts_data(request):
    result = literal_eval(ssh_exec(k8s_host, k8s_port ,'python /work/spark_scripts/tasks/script_list.py script'))
    return HttpResponse(json.dumps({'code': -1, 'tableData': result}), content_type='application/json;charset = utf-8')



@login_required
def task_schedule_scripts_add(request):
    try:
        data = json.loads(request.body)
        script_name = data.get('script_name')
        script_content = data.get('script_content')
        # 过滤危险的rm命令
        if 'rm ' in script_content:
            return HttpResponse(json.dumps({'code': 1, 'msg': '有危险命令'}), content_type="application/json")
        # 限制k8s_user账号所使用的标签
        if request.user.username == 'k8s_user' and not 'spark.kubernetes.node.selector.task=temp01' in script_content:
            return HttpResponse(json.dumps({'code': 1, 'msg': '标签选择器配置错误'}), content_type="application/json")
        # 本地写缓存文件
        with open('/tmp/tempfile', 'w') as f:
            f.write(script_content)
        # 缓存文件拷贝到远程
        code = subprocess.call(f'scp -P {k8s_port} /tmp/tempfile {k8s_host}:/work/spark_scripts/tasks/{script_name}', shell=True)
        if code != 0 :
            return HttpResponse(json.dumps({'code': 1, 'msg': '传输文件错误'}), content_type="application/json")
        return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_schedule_scripts_edit(request):
    try:
        data = json.loads(request.body)
        script_name = data.get('script_name')
        # 拷贝远程脚本到本地缓存文件
        code = subprocess.call(f'scp -P {k8s_port} {k8s_host}:/work/spark_scripts/tasks/{script_name} /tmp/tempfile', shell=True)
        if code != 0 :
            return HttpResponse(json.dumps({'code': 1, 'msg': '传输文件错误'}), content_type="application/json")
        # 读缓存文件内容返回前端
        with open('/tmp/tempfile') as f:
            content = f.read()
        return HttpResponse(json.dumps({'code':10, 'script_name': script_name, 'script_content': content}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
@require_websocket
def task_schedule_scripts_run(request):
    message = request.websocket.wait()
    message = json.loads(message)
    script_name = message.get('script_name')
    status = message.get('status')
    # 运行远程脚本
    p = subprocess.Popen(f'ssh {k8s_host} -p {k8s_port} "/bin/bash /work/spark_scripts/tasks/{script_name}"', shell=True, stdout=subprocess.PIPE)
    # 启动线程监听websocket信号，获取到stop则停止远程脚本，超5分钟自杀
    def recive_data(request, p):
        i = 0
        while 1:
            if i > 86400: sys.exit(1)
            data = request.websocket.wait()
            data = json.loads(data)
            if data.get('status') == 'stop':
                p.kill()
                sys.exit(0)
            time.sleep(1)
    t = Thread(target=recive_data, args=(request, p))
    t.start()
    # 持续获取远程脚本输出，通过websocket发送到前端
    while p.poll() == None:
        line = p.stdout.readline().decode()
        if line:
            request.websocket.send(json.dumps(line))



@login_required
def task_schedule_config(request):
    path = request.path.split('/')[1]
    return render(request, 'task_schedule/task_schedule_config.html', {'user': request.user.username,
                                                                        'path1': 'task_schedule',
                                                                        'path2': path,
                                                                        'page_name1': u'任务调度',
                                                                        'page_name2': '配置文件'})



@login_required
def task_schedule_config_data(request):
    result = literal_eval(ssh_exec(k8s_host, k8s_port, 'python /work/spark_scripts/tasks/script_list.py config'))
    return HttpResponse(json.dumps({'code': -1, 'tableData': result}), content_type='application/json;charset = utf-8')



@login_required
def task_schedule_config_add(request):
    try:
        data = json.loads(request.body)
        config_name = data.get('config_name')
        config_content = data.get('config_content')
        # 判断文件名后缀
        if config_name.endswith('properties'):
            # 本地写缓存文件
            with open('/tmp/tempfile', 'w') as f:
                f.write(config_content)
            # 缓存文件拷贝到远程
            code = subprocess.call(f'scp -P {k8s_port} /tmp/tempfile {k8s_host}:/work/www/spark/conf/{config_name}', shell=True)
            if code != 0 :
                return HttpResponse(json.dumps({'code': 1, 'msg': '传输文件错误'}), content_type="application/json")
            return HttpResponse(json.dumps({'code':0,'msg':'操作成功'}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'code': 1, 'msg': '文件后缀错误'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_schedule_config_edit(request):
    try:
        data = json.loads(request.body)
        config_name = data.get('config_name')
        # 拷贝远程脚本到本地缓存文件
        code = subprocess.call(f'scp -P {k8s_port} {k8s_host}:/work/www/spark/conf/{config_name} /tmp/tempfile', shell=True)
        if code != 0 :
            return HttpResponse(json.dumps({'code': 1, 'msg': '传输文件错误'}), content_type="application/json")
        # 读缓存文件内容返回前端
        with open('/tmp/tempfile') as f:
            content = f.read()
        return HttpResponse(json.dumps({'code':10, 'config_name': config_name, 'config_content': content}),content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'code': 1, 'msg': e}), content_type="application/json")



@login_required
def task_schedule_upload(request):
    path = request.path.split('/')[1]
    return render(request, 'task_schedule/task_schedule_update.html', {'user': request.user.username,
                                                               'path1': 'task_schedule',
                                                               'path2': path,
                                                               'page_name1': u'task_schedule',
                                                               'page_name2': '上传jar包'})



@login_required
def task_schedule_upload_data(request):
    # 接收文件
    file = request.FILES.get('image', None)
    backup = request.POST.get('backup', None)
    filename = re.sub(r'\(\d+\)', '', file.name)

    with open(f'/tmp/{filename}', 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    # 复制文件到k8s机器
    remote_jar_dir = '/work/www/spark/jar/'
    if backup != None and backup == 'true':
        # 备份远程jar包
        print(f'ssh {k8s_host} -p {k8s_port} "\mv {remote_jar_dir}{filename}{{,_bak}}"')
        p0 = subprocess.Popen(f'ssh {k8s_host} -p {k8s_port} "\mv {remote_jar_dir}{filename}{{,_bak}}"',
                          shell=True, stdout=subprocess.PIPE)
        p0.wait()
    # 上传jar包
    print(f'scp -P {k8s_port} /tmp/{filename} {k8s_host}:{remote_jar_dir}')
    p1 = subprocess.Popen(f'scp -P {k8s_port} /tmp/{filename} {k8s_host}:{remote_jar_dir}',
                         shell=True, stdout=subprocess.PIPE)
    p1.wait()

    return HttpResponse(json.dumps({'code': 0, 'msg': '上传成功'}), content_type="application/json")



@login_required
def task_schedule_tasks(request):
    path = request.path.split('/')[1]
    return render(request, 'task_schedule/task_schedule_tasks.html', {'user': request.user.username,
                                                               'path1': 'task_schedule',
                                                               'path2': path,
                                                               'page_name1': u'task_schedule',
                                                               'page_name2': '运行中任务'})



@login_required
def task_schedule_tasks_data(request):
    data = json.loads(request.body)
    radio = data.get('radio')
    result = literal_eval(ssh_exec(k8s_host, k8s_port ,f'python /work/spark_scripts/tasks/script_list.py tasks {radio}'))
    return HttpResponse(json.dumps({'code': -1, 'tableData': result}), content_type='application/json;charset = utf-8')



@login_required
def task_schedule_task_stop(request):
    # 停止k8s指定pod
    data = json.loads(request.body)
    task_name = data.get('task_name')
    # 带上k8s环境变量删除pod
    code = subprocess.call(f'ssh {k8s_host} -p {k8s_port} "export KUBECONFIG=/etc/kubernetes/admin.conf; /usr/bin/kubectl delete pod {task_name}"', shell=True)
    if code != 0:
        return HttpResponse(json.dumps({'code': 1, 'msg': '停止失败'}), content_type="application/json")
    return HttpResponse(json.dumps({'code': 0, 'msg': '停止成功'}), content_type="application/json")



@login_required
@require_websocket
def task_schedule_task_log(request):
    message = request.websocket.wait()
    message = json.loads(message)
    task_name = message.get('task_name')
    # 远程获取pod日志
    p = subprocess.Popen(f'ssh {k8s_host} -p {k8s_port} "export KUBECONFIG=/etc/kubernetes/admin.conf; /usr/bin/kubectl logs -f {task_name}"',
                         shell=True, stdout=subprocess.PIPE)
    # 启动线程监听websocket信号，获取到stop则停止远程脚本，超5分钟自杀
    def recive_data(request, p):
        i = 0
        while 1:
            if i > 300:
                sys.exit(1)
            data = request.websocket.wait()
            if data:
                data = json.loads(data)
                if data.get('status') == 'stop':
                    p.kill()
                    sys.exit(0)
                time.sleep(1)

    t = Thread(target=recive_data, args=(request, p))
    t.start()
    # 初始化计时器
    my_timer = timer(0.4)
    # 持续获取日志输出，通过websocket发送到前端
    data = ''
    # 第一行标记
    is_first_line = 1
    # 当命令未完成或者数据没读完时，持续获取并发送数据
    while p.poll() == None or line != None:
        # 设置文件句柄为非阻塞
        fcntl.fcntl(p.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        try:
            line = p.stdout.readline().decode()
        except IOError:
            time.sleep(1)
            continue
        # 判断是否第一行，第一行开始计时
        if is_first_line == 1:
            my_timer.time_start()
            is_first_line = 0
        data += line
        # 判断计时器到预设时间
        if my_timer.is_ready():
            if data:
                request.websocket.send(json.dumps(data))
                data = ''
                my_timer.time_start()
        time.sleep(0.004)



@login_required
def task_schedule_task_sparkui(request):
    # 启动隧道
    ssh_server.start()
    # 通过SSH隧道开启本地sparkui监听
    data = json.loads(request.body)
    task_name = data.get('task_name')
    # 检测SSH隧道是否可用,不可用重启
    if not ssh_server.is_alive:
        ssh_server.restart()
    # 清理并打开远程sparkui
    subprocess.Popen(
        f'''ssh {k8s_host} -p {k8s_port} "export KUBECONFIG=/etc/kubernetes/admin.conf; \
            ps aux|grep port-forward|grep -v grep|awk '{{print \$2}}'|xargs kill -9; \
            /usr/bin/kubectl port-forward {task_name} 4040:4040" ''',
        shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    return HttpResponse(json.dumps({'code': 10, 'msg': '开启成功'}), content_type="application/json")



@login_required
def task_schedule_task_download(request):
    # 日志下载
    data = json.loads(request.body)
    task_name = data.get('task_name')
    # 日志保存到远程本地缓存
    code = subprocess.call(f'ssh {k8s_host} -p {k8s_port} "export KUBECONFIG=/etc/kubernetes/admin.conf; \
                           /usr/bin/kubectl logs {task_name} > /tmp/logstempfile.txt"', shell=True)
    if code != 0:
        return HttpResponse(json.dumps({'code': 1, 'msg': '日志文件转储失败'}), content_type="application/json")
    # 日志传输至本地缓存
    code = subprocess.call(f'scp -P {k8s_port} {k8s_host}:/tmp/logstempfile.txt \
                           /usr/share/nginx/BearCatOMS_v2/static/logstempfile.txt', shell=True)
    if code != 0:
        return HttpResponse(json.dumps({'code': 1, 'msg': '日志文件传输失败'}), content_type="application/json")
    return HttpResponse(json.dumps({'code': 11, 'msg': '成功'}), content_type="application/json")