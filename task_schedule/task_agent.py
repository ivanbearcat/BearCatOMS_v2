#!python
# -*- coding: utf-8 -*-
import SocketServer
import time
import json
import subprocess
from threading import Thread
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def run_task(self, recv_data):
        # 创建临时脚本
        tmp_file = '/tmp/{0}{1}'.format(recv_data["name"], recv_data["suffix"])
        with open(tmp_file, 'w') as f:
            f.write(recv_data["cmd"])
        # 清理旧日志
        if os.path.exists('/tmp/{0}.log'.format(recv_data["name"])):
            os.remove('/tmp/{0}.log'.format(recv_data["name"]))
        # 脚本开始时间
        start_time = time.time()
        # 执行脚本
        print('{0} {1} > /tmp/{2}.log 2>&1'.format(recv_data["bin"], tmp_file, recv_data["name"]))
        p = subprocess.Popen('{0} {1} > /tmp/{2}.log 2>&1'.format(recv_data["bin"], tmp_file, recv_data["name"]),
                             shell=True)
        # 等待执行完成记录时间和退出码
        code = p.wait()
        stop_time = time.time()
        duration = str(stop_time - start_time)
        with open('/tmp/{0}.log'.format(recv_data["name"]), 'a') as f:
            f.write('\ndone {0} {1}'.format(code, duration))

    def handle(self):
        recv_data_json = ''
        while 1:
            try:
                r_data = self.request.recv(1024)
            except Exception:
                break
            recv_data_json += r_data.decode()
            self.request.setblocking(0)
            time.sleep(0.1)

        print("from: %s " % self.client_address[0])
        # 真实数据
        recv_data = json.loads(recv_data_json)
        # 运行脚本
        Thread(target=self.run_task, args=(recv_data,)).start()
        # 返回值
        self.request.sendall(json.dumps(0).encode())


if __name__ == "__main__":
    HOST,PORT = "localhost",9999
    server = SocketServer.ThreadingTCPServer((HOST,PORT),MyTCPHandler)
    server.serve_forever()