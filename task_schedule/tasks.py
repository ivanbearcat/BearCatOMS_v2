from __future__ import absolute_import, unicode_literals
from celery import shared_task
from task_schedule.models import single_tasks, task_group
from django.http import HttpResponse
import json
from task_schedule.apps import type_dict
from commons.socket_send_data import tunnel_send
import datetime
import subprocess
import time
import threading
from ast import literal_eval


@shared_task(bind=True)
def run_task(self, task_name):
    orm = single_tasks.objects.get(task_name=task_name)
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
        if self.request.id:
            orm.task_id = self.request.id
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


    host = orm.target.split(':')[0]
    port = orm.target.split(':')[1]




@shared_task(bind=True)
def run_tasks(self, group_name):
    orm = task_group.objects.get(group_name=group_name)
    task_names = literal_eval(orm.group_content)
    orm.last_run_time = datetime.datetime.now()
    orm.status = '运行中'
    orm.task_id = self.request.id
    orm.save()
    time_begin = time.time()
    for i in task_names:
        orm = task_group.objects.get(group_name=group_name)
        orm.task_now = i
        orm.save()
        run_task(i)
        # 判断单个任务是否运行完
        orm = single_tasks.objects.get(task_name=i)
        host = orm.target.split(':')[0]
        port = int(orm.target.split(':')[1])
        while 1:
            try:
                p = subprocess.Popen(f'ssh {host} -p {port} "tail -1 /tmp/{orm.task_name}.log"', shell=True,
                                     stdout=subprocess.PIPE)
                p.wait()
                stdout, stderr = p.communicate()
                if stdout == b'':
                    break
                stdout_list = stdout.decode().strip().split()
                if len(stdout_list) == 3 and stdout_list[0] == 'done':
                    break
                else:
                    time.sleep(5)
            except Exception:
                break
    orm = task_group.objects.get(group_name=group_name)
    orm.status = '已完成'
    orm.duration = str(time.time() - time_begin)
    orm.save()