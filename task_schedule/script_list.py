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
                

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'script':
            fetch_script()
        if sys.argv[1] == 'config':
            fetch_config()
    else:
        print('no args')
