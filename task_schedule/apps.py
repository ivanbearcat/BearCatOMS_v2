from django.apps import AppConfig
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render
from sshtunnel import SSHTunnelForwarder


type_dict = {
            'k8s-shell': {
                'suffix': '.sh',
                'bin': '/bin/bash'
            },
            'shell': {
                'suffix': '.sh',
                'bin': '/bin/bash'
            },
            'python': {
                'suffix': '.py',
                'bin': '/usr/local/python36/bin/python3'
            }
        }

k8s_host = '113.107.166.14'
k8s_port = 15231
# 建立SparkUI的SSH隧道
ssh_server = SSHTunnelForwarder((k8s_host, k8s_port),
                                ssh_pkey="/root/.ssh/id_rsa",
                                remote_bind_address=('127.0.0.1', 4040),
                                local_bind_address=('0.0.0.0', 4040))

class k8s_user_perm_middleware(MiddlewareMixin):
    def process_request(self, request):
        # 限制k8s_user对视图的访问权限
        if  request.user.username == 'k8s_user':
            if request.path in ['/home/',
                                '/logout/',
                                '/task_schedule_scripts/',
                                '/task_schedule_scripts_data/',
                                '/task_schedule_scripts_add/',
                                '/task_schedule_scripts_edit/',
                                '/task_schedule_scripts_run/',
                                '/task_schedule_config/',
                                '/task_schedule_config_data/',
                                '/task_schedule_config_add/',
                                '/task_schedule_config_edit/',
                                '/task_schedule_upload/',
                                '/task_schedule_upload_data/',
                                '/task_schedule_tasks/',
                                '/task_schedule_tasks_data/',
                                '/task_schedule_task_stop/',
                                '/task_schedule_task_log/',
                                '/task_schedule_task_sparkui/']:
                return None
            else:
                return render(request, '404.html')
        else:
            return None

class TaskScheduleConfig(AppConfig):
    name = 'task_schedule'
