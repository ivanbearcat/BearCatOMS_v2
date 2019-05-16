# -*- coding: utf-8 -*-
import socket
import time
from sshtunnel import SSHTunnelForwarder
import json

def tunnel_send(host, port, data):
    server = SSHTunnelForwarder(
        (host, port),
        ssh_pkey="/root/.ssh/id_rsa",
        remote_bind_address=('127.0.0.1', 9999)
    )
    server.start()
    addr = ('127.0.0.1', server.local_bind_port)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(addr)
    recv_data_json = ''
    data_json_Byte = json.dumps(data).encode()
    s.sendall(data_json_Byte)

    while 1:
        try:
            r_data = s.recv(1024)
            if not r_data:
                break
            recv_data_json += r_data.decode()
            s.setblocking(0)
            time.sleep(0.1)
        except BlockingIOError:
            continue
    if not recv_data_json:
        return 0
    recv_data = json.loads(recv_data_json)
    s.close()
    server.close()
    return recv_data