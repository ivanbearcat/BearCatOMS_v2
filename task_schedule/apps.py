from django.apps import AppConfig

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

class TaskScheduleConfig(AppConfig):
    name = 'task_schedule'
