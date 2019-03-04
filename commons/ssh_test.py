import paramiko


def test(hostname, username, password):
    try:
        ssh=paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password, timeout=2)
        ssh.close()
        print('secuess')
        return True
    except Exception as e:
        print(f'fail: {e}')
        return False
