#!python
from libs.libs import run_shell

class gather_disk(object):
    # 获取磁盘信息
    def start(self):
        print('get disk')
        data_list = []
        # 获取根磁盘UUID
        code, name = run_shell('lsblk |grep disk')
        data = name if code == 0 else ''
        for i in data.split('\n'):
            name = i.split()[0]
            size = i.split()[3]
            data_list.append({'name': name, 'size': size})
        return data_list