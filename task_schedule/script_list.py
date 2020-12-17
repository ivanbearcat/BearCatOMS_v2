#!python
#coding:utf8
import os
import re
import subprocess
import sys

script_dir = '/work/spark_scripts/tasks'
config_dir = '/work/www/spark/conf'
data_list = []

def fetch_script():
    # 获取脚本
    # 按时间倒序列出文件
    p = subprocess.Popen('ls -t {0}|tac'.format(script_dir), shell=True, stdout=subprocess.PIPE)
    p.wait()
    items, _ = p.communicate()
    for i in items.split('\n'):
        # 获取目录下以sh结尾的文件
        if os.path.isfile(os.path.join(script_dir, i)) and i.endswith('sh'):
            data_dict = {}
            data_dict['script_name'] = i
            # 读文件内容
            with open(os.path.join(script_dir, i)) as f:
                data = f.read()
                # 正则获取jar包名
                package_name_re = re.search(r'[^#]http.*/(.*jar)', data)
                if package_name_re:
                    package_name = package_name_re.group(1)
                    data_dict['package_name'] = package_name
                else:
                    data_dict['package_name'] = ''
                # 正则获取类名
                class_name_re = re.search(r'--class\s+(.*)\s+\\', data)
                if class_name_re:
                    class_name = class_name_re.group(1)
                    data_dict['class_name'] = class_name
                else:
                    data_dict['class_name'] = ''
            data_list.append(data_dict)
    print(data_list)

def fetch_config():
    # 获取配置文件
    # 按时间倒序列出文件
    p = subprocess.Popen('ls -t {0}|tac'.format(config_dir), shell=True, stdout=subprocess.PIPE)
    p.wait()
    items, _ = p.communicate()
    for i in items.split('\n'): 
        # 获取目录下以properties结尾的文件
        if os.path.isfile(os.path.join(config_dir, i)) and i.endswith('properties'):
            data_dict = {}
            data_dict['config_name'] = i
            data_list.append(data_dict)
    print(data_list)

def fetch_tasks(status):
    # 获取任务
    # 增加k8s的环境变量，不然无法使用kubectl命令
    os.environ['KUBECONFIG'] = '/etc/kubernetes/admin.conf'
    # 获取k8s正在运行的任务名和已运行时间
    p = subprocess.Popen('''kubectl get pod|grep %s|grep -v exec|awk '{print $1" "$5}' ''' % (status), shell=True, stdout=subprocess.PIPE)
    while p.poll() != None:
        time.sleep(0.1)
    items, _ = p.communicate()
    for i in items.strip().split('\n'):
        # 获取结尾的文件
        data_dict = {}
        data_dict['task_name'] = i.split()[0]
        # 换算成秒
        run_seconds = i.split()[1]
        run_seconds = run_seconds.replace('s','')
        run_seconds = run_seconds.replace('m','*60+')
        run_seconds = run_seconds.replace('h','*3600+')
        run_seconds = run_seconds.replace('d','*86400+')
        if run_seconds[-1] == '+':
            run_seconds = run_seconds[:-1]
        run_seconds = eval(run_seconds)
        data_dict['task_time'] = run_seconds
        data_list.append(data_dict)
    print(data_list)
                

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'script':
            fetch_script()
        if sys.argv[1] == 'config':
            fetch_config()
        if sys.argv[1] == 'tasks':
            fetch_tasks(sys.argv[2])
    else:
        print('no args')
