"""BearCatOMSv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from login.views import *
from home.views import *
from user_manage.views import *
from server_info.views import *
from operation.views import *
from monitor.views import *
from audit.views import *
from task_schedule.views import *
from ansiable.views import *
from gitlab_hook.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', login),
    url(r'^login_auth/', login_auth),
    url(r'^logout/', logout),
    url(r'^accounts/login/$', not_login),
    url(r'^home/', home),
    url(r'^chpasswd/', chpasswd),
    url(r'^post_chpasswd/', post_chpasswd),
    url(r'^zabbix/', zabbix),
    url(r'^zabbix_guild/', zabbix_guild),
    url(r'^grafana/', grafana),
    url(r'^server_info_table/', server_info_table),
    url(r'^server_info_data/', server_info_data),
    url(r'^server_info_save/', server_info_save),
    url(r'^server_info_del/', server_info_del),
    url(r'^server_info_table_new/', server_info_table_new),
    url(r'^server_table_data/', server_table_data),
    url(r'^server_table_save/', server_table_save),
    url(r'^domain_name_CRT_table/', domain_name_CRT_table),
    url(r'^domain_name_CRT_data/', domain_name_CRT_data),
    url(r'^cmd_template/', cmd_template),
    url(r'^cmd_template_data/', cmd_template_data),
    url(r'^cmd_template_dropdown/', cmd_template_dropdown),
    url(r'^cmd_template_save/', cmd_template_save),
    url(r'^cmd_template_del/', cmd_template_del),
    url(r'^server_operation/', server_operation),
    url(r'^get_server_list/', get_server_list),
    url(r'^search_server_list/', search_server_list),
    url(r'^audit_log/', audit_log),
    url(r'^audit_get_data/', audit_get_data),
    url(r'^audit_log_data/', audit_log_data),
    url(r'^task_table/', task_table),
    url(r'^task_table_data/', task_table_data),
    url(r'^task_table_save/', task_table_save),
    url(r'^task_table_del/', task_table_del),
    url(r'^task_table_run/', task_table_run),
    url(r'^task_table_kill/', task_table_kill),
    url(r'^log_web_socket/', log_web_socket),
    url(r'^task_table_group/', task_table_group),
    url(r'^task_table_group_data/', task_table_group_data),
    url(r'^task_table_group_save/', task_table_group_save),
    url(r'^task_table_group_del/', task_table_group_del),
    url(r'^task_table_group_run/', task_table_group_run),
    url(r'^task_table_group_kill/', task_table_group_kill),
    url(r'^task_schedule_table/', task_schedule_table),
    url(r'^task_schedule_data/', task_schedule_data),
    url(r'^task_schedule_save/', task_schedule_save),
    url(r'^task_schedule_switch/', task_schedule_switch),
    url(r'^task_schedule_del/', task_schedule_del),
    url(r'^task_schedule_scripts/', task_schedule_scripts),
    url(r'^task_schedule_scripts_data/', task_schedule_scripts_data),
    url(r'^task_schedule_scripts_add/', task_schedule_scripts_add),
    url(r'^task_schedule_scripts_edit/', task_schedule_scripts_edit),
    url(r'^task_schedule_scripts_run/', task_schedule_scripts_run),
    url(r'^task_schedule_config/', task_schedule_config),
    url(r'^task_schedule_config_data/', task_schedule_config_data),
    url(r'^task_schedule_config_add/', task_schedule_config_add),
    url(r'^task_schedule_config_edit/', task_schedule_config_edit),
    url(r'^task_schedule_upload/', task_schedule_upload),
    url(r'^task_schedule_upload_data/', task_schedule_upload_data),
    url(r'^task_schedule_tasks/', task_schedule_tasks),
    url(r'^task_schedule_tasks_data/', task_schedule_tasks_data),
    url(r'^task_schedule_task_stop/', task_schedule_task_stop),
    url(r'^task_schedule_task_log/', task_schedule_task_log),
    url(r'^task_schedule_task_sparkui/', task_schedule_task_sparkui),
    url(r'^task_schedule_task_download/', task_schedule_task_download),
    url(r'^ansiable_playbook/', ansiable_playbook),
    url(r'^ansiable_playbook_data/', ansiable_playbook_data),
    url(r'^ansiable_playbook_run/', ansiable_playbook_run),
    url(r'^ansiable_playbook_config_edit/', ansiable_playbook_config_edit),
    url(r'^ansiable_playbook_change_branch/', ansiable_playbook_change_branch),
    url(r'^ansiable_playbook_log/', ansiable_playbook_log),
    url(r'^ansiable_playbook_log_data/', ansiable_playbook_log_data),
    url(r'^upload/', upload),
    url(r'^quick_update/', quick_update),
    url(r'^web_hook_api/', web_hook_api),
]
