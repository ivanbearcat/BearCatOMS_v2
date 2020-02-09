#!python
import os
import yaml

playbook_dir = '/root/playbooks'
roles_dir = '/etc/ansible/roles'
data_list = []
for path, sub_path, files in os.walk(playbook_dir):
    for i in files:
        if i.endswith('yaml'):
            data_dict = {}
            data_dict['playbook_path'] = os.path.join(path, i)
            with open(os.path.join(path, i)) as f1:
                data = yaml.load(f1)
                for j in data:
                    try:
                        if not j['hosts'] == 'myself':
                            roles = j['roles'][0]
                            vars_files = j['vars_files'][0]
                            data_dict['vars_files'] = vars_files
                            with open(vars_files) as f2:
                                vars_data = yaml.load(f2)
                                if vars_data.get('project'):
                                    data_dict['project_name'] = vars_data.get('project')
                                else:
                                    data_dict['project_name'] = ''
                                if vars_data.get('branch'):
                                    data_dict['branch'] = vars_data.get('branch')
                                else:
                                    data_dict['branch'] = ''
                                if vars_data.get('source_config_file'):
                                    data_dict['config_file'] = os.path.join(roles_dir, roles, 'files', vars_data['source_config_file'])
                                else:
                                    data_dict['config_file'] = ''
                                
                    except Exception as e:
                        break
            if len(data_dict) == 5:
                data_list.append(data_dict)
print data_list
                           
                            
