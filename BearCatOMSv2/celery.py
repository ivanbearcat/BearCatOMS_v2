from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# 设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BearCatOMSv2.settings')
app = Celery('BearCatOMSv2')
# 使用CELERY_ 作为前缀，在settings中写配置
app.config_from_object('django.conf:settings', namespace='CELERY')
# 发现任务文件每个app下的task.py
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))