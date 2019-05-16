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

class TaskScheduleConfig(AppConfig):
    name = 'task_schedule'
