#!python
from libs.libs import run_shell

class gather_nic(object):
    # 获取网卡信息
    def start(self):
        print('get nic')
        data = []

        cmd1 = '''ip addr|grep 'state UP'|awk -F':' '{print $2}' '''
        code, result = run_shell(cmd1)
        data1 = result if code == 0 else ''

        cmd2 = '''ip addr|grep 'state UP' -A1|grep 'link/ether'|awk '{print $2}' '''
        code, result = run_shell(cmd2)
        data2 = result if code == 0 else ''

        cmd3 = '''ip addr|grep 'state UP' -A2|grep 'inet'|awk '{print $2}'|awk -F'/' '{print $1}' '''
        code, result = run_shell(cmd3)
        data3 = result if code == 0 else ''

        cmd4 = '''ip addr|grep 'state UP' -A2|grep 'inet'|awk '{print $2}'|awk -F'/' '{print $2}' '''
        code, result = run_shell(cmd4)
        data4 = result if code == 0 else ''