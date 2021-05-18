#!python
from libs.libs import run_shell

class gather_basic(object):
    # 获取主机基础信息
    def start(self):
        print('get basic')
        data = {}
        # 获取根磁盘UUID作为服务器UUID
        cmd = '''df -h|grep -w /|awk '{print $1}'|xargs blkid|awk '{print $2}'|awk -F'"' '{print $2}' '''
        code, UUID = run_shell(cmd)
        data['UUID'] = UUID if code == 0 else ''
        # 获取hostname
        code, hostname = run_shell('hostname')
        data['hostname'] = hostname if code == 0 else ''
        # 获取系统发行版
        cmd = '''lsb_release -d|awk -F':' '{print $2}' '''
        code, os = run_shell(cmd)
        data['os'] = os if code == 0 else ''
        # 获取内核版本
        code, kernel_version = run_shell('uname -r')
        data['kernel_version'] = kernel_version if code == 0 else ''
        # 获取CPU数量
        cmd = '''lscpu |grep 'CPU(s):'|grep -v 'NUMA'|awk '{print $2}' '''
        code, cpu_count = run_shell(cmd)
        data['cpu_count'] = cpu_count if code == 0 else ''
        # 获取CPU型号
        cmd = '''lscpu|grep 'Model name'|awk -F':' '{print $2}' '''
        code, cpu_model = run_shell(cmd)
        data['cpu_model'] = cpu_model if code == 0 else ''

        return data