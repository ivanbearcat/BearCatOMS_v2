import paramiko
import os

def ssh_exec(ip, port, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    privatekey = os.path.expanduser('/root/.ssh/id_rsa')
    key = paramiko.RSAKey.from_private_key_file(privatekey)
    ssh.connect(ip, port=port, username="root", pkey=key)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    return ssh_stdout.read().decode()