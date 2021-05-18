from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(server)
admin.site.register(disk)
admin.site.register(memory)
admin.site.register(NIC)
admin.site.register(server_group)



import xadmin
# 引入要管理的模型类
from xadmin import views


# # Register your models here.
class serverAdmin(object):
    # 列表页属性
    list_display = ['UUID', 'hostname', 'os', 'kernel_version', 'cpu_count', 'cpu_model', 'cabinet_info', 'ssh_ip',
                    'ssh_port', 'ssh_user', 'ssh_pass', 'update_time', 'comment']
    list_filter = ['UUID', 'hostname', 'os', 'kernel_version', 'cpu_count', 'cpu_model', 'cabinet_info', 'ssh_ip',
                    'ssh_port', 'ssh_user', 'ssh_pass', 'update_time', 'comment']
    search_fields = ["UUID"]
    list_per_page = 10

    # 相应表图标配置
    # https://fontawesome.com/icons
    model_icon = 'glyphicon glyphicon-cloud'
    # 显示详情
    show_detail_fields = ['UUID']
    # 数据刷新时间
    refresh_times = (3, 5)

    # 执行动作框的位置
    actions_on_top = False
    actions_on_bottom = True


class diskAdmin(object):
    # 列表页属性
    list_display = ['slot', 'model', 'size', 'type', 'server']
    list_filter = ['slot', 'model', 'size', 'type', 'server']
    search_fields = ["slot"]
    list_per_page = 10

    # 相应表图标配置
    # https://fontawesome.com/icons
    model_icon = 'glyphicon glyphicon-hdd'
    # 显示详情
    show_detail_fields = ['slot']
    # 数据刷新时间
    refresh_times = (3, 5)

    # 执行动作框的位置
    actions_on_top = False
    actions_on_bottom = True


class memoryAdmin(object):
    # 列表页属性
    list_display = ['slot', 'model', 'size', 'sn', 'server']
    list_filter = ['slot', 'model', 'size', 'sn', 'server']
    search_fields = ["slot"]
    list_per_page = 10

    # 相应表图标配置
    # https://fontawesome.com/icons
    model_icon = 'glyphicon glyphicon-credit-card'
    # 显示详情
    show_detail_fields = ['slot']
    # 数据刷新时间
    refresh_times = (3, 5)

    # 执行动作框的位置
    actions_on_top = False
    actions_on_bottom = True


class NICAdmin(object):
    # 列表页属性
    list_display = ['name', 'mac', 'ipaddr', 'netmask', 'server']
    list_filter = ['name', 'mac', 'ipaddr', 'netmask', 'server']
    search_fields = ["name"]
    list_per_page = 10

    # 相应表图标配置
    # https://fontawesome.com/icons
    model_icon = 'fa fa-circle'
    # 显示详情
    show_detail_fields = ['name']
    # 数据刷新时间
    refresh_times = (3, 5)

    # 执行动作框的位置
    actions_on_top = False
    actions_on_bottom = True


class server_groupAdmin(object):
    # 列表页属性
    list_display = ['name', 'server']
    list_filter = ['name', 'server']
    search_fields = ["name"]
    list_per_page = 10

    # 相应表图标配置
    # https://fontawesome.com/icons
    model_icon = 'fa fa-users'
    # 显示详情
    show_detail_fields = ['name']
    # 数据刷新时间
    refresh_times = (3, 5)

    # 执行动作框的位置
    actions_on_top = False
    actions_on_bottom = True


class BaseSetting(object):
    '''
    主题样式多样化
    '''
    enable_themes = True
    use_bootswatch = True


# 设置全局图标
# http://v3.bootcss.com/components/
# http://www.yeahzan.com/fa/facss.html
class GlobalSetting(object):
    # 页头
    site_title = 'CMDB'
    # 页脚
    site_footer = 'BearCat'
    # 左侧栏折叠样式
    # menu_style = 'accordion'


xadmin.site.register(server, serverAdmin)
xadmin.site.register(disk, diskAdmin)
xadmin.site.register(memory, memoryAdmin)
xadmin.site.register(NIC, NICAdmin)
xadmin.site.register(server_group, server_groupAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
