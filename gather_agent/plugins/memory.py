#!python
from libs.libs import run_shell

class gather_memory(object):
    # 获取内存信息
    def start(self):
        print('get memory')
        #获取内存大小
        cmd1 = '''dmidecode|grep -P -A8 "Memory\s+Device"|grep -v Range|grep -v 'Size: No Module Installed'|egrep 'Size' -A3|grep Size|awk -F':' '{print $2}' '''
        code, result = run_shell(cmd1)
        data1 = result if code == 0 else ''
        #获取内存插槽信息
        cmd2 = '''dmidecode|grep -P -A8 "Memory\s+Device"|grep -v Range|grep -v 'Size: No Module Installed'|egrep 'Size' -A3|grep Locator|awk -F':' '{print $2}' '''
        code, result = run_shell(cmd2)
        data2 = result if code == 0 else ''
        data = list(zip(data1.split('\n'), data2.split('\n')))
        data_list = []
        for i in data:
            data_list.append({'size': i[0], 'slot': i[1]})
        return data_list