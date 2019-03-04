import yaml
import subprocess

check_profile_result_yaml = subprocess.check_output("/usr/bin/salt-ssh '*' -r 'grep upload_history.py /etc/profile' --out=yaml", shell=True)
check_profile_result_dict = yaml.load(check_profile_result_yaml)

check_uploadfile_result_yaml = subprocess.check_output("/usr/bin/salt-ssh '*' -r 'test -f /usr/local/script/upload_history.py' --out=yaml", shell=True)
check_uploadfile_result_dict = yaml.load(check_uploadfile_result_yaml)

add_audit_list = []
for k,v in check_profile_result_dict.items():
	if v['retcode'] == 1:
		add_audit_list.append(k)
for k,v in check_uploadfile_result_dict.items():
	if v['retcode'] == 1:
		if k not in add_audit_list:
			add_audit_list.append(k)
			
add_audit_str = ','.join(add_audit_list)
add_audit_code = subprocess.call(f"/usr/bin/salt-ssh -L '{add_audit_str}' state.sls add_audit.init", shell=True) 

for i in add_audit_list:
    subprocess.call(f'''/usr/bin/salt-ssh '{i}' file.replace /usr/local/script/upload_history.py pattern="application = ''" repl="application = '{i}'" ''', shell=True)  

#i='Monitor'
#subprocess.call(f'''/usr/bin/salt-ssh '{i}' file.replace /usr/local/script/upload_history.py pattern="application = ''" repl="application = '{i}'" ''', shell=True)  
