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
from java_info.views import *


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
    url(r'^java_info_table/', java_info_table),
]
