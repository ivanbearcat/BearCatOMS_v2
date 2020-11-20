#!python
import os
import re

file_dir = '/work/spark_scripts/tasks'
data_list = []

for i in os.listdir(file_dir):
    if os.path.isfile(i) and i.endswith('sh'):
        print(i)
        data_dict = {}
        data_dict['script_name'] = i
        with open(os.path.join(file_dir, i)) as f:
            data = f.read()
            package_name_re = re.search(r'[^#]http.*/(.*jar)', data)
            if package_name_re:
                package_name = package_name_re.group(1)
                data_dict['package_name'] = package_name
            else:
                continue
            class_name_re = re.search(r'--class\s+(.*)\s+\\', data)
            if class_name_re:
                class_name = class_name_re.group(1)
                data_dict['class_name'] = class_name
            else:
                continue
        data_list.append(data_dict)
        
print(data_list)
