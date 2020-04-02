import sys
sys.path.append('..')
import pexpect
import os
from Config.get_all_config import *

model = sys.argv[1]
image = sys.argv[2]
status_file = sys.argv[3]

ssh_newkey = 'Are you sure you want to continue connecting'
ssh_cmd = 'ssh '+username+'@'+mgmt_ip
ssh_cmd += ' -o StrictHostKeyChecking=no'

class Connect_DUT():
	def __init__ (self):
		self.model = ''
		self.image_version = ''
		self.image_url = 'http://192.168.40.82:8080/job/' + self.image_version + '/artifact/target/sonic-broadcom.bin'
		self.status_file = ''
		self.status = open(status_file,'wb')
		self.DUT_init = self.get_DUT_information
		self.mgmt_ip = ''
		self.hostname = ''
		self.username = ''
		self.password = ''
		self.prompt = r'\$'
		self.client = ''

	def get_DUT_information(self):
		for model_info in model_info_list :
			if model_info['Model'] == self.model:
				self.mgmt_ip = model_info['Mgmt_ip']
				self.hostname = model_info['Hostname']
				self.username = model_info['Username']
				self.password = model_info['Password']

	def remove_old_ssh_key(self):
		os.system('ssh key-gen -R "'+self.mgmt_ip+'"')

	def login_DUT(self):
		self.client = pexpect.spawn(ssh_cmd)
		self.client.logfile = self.status
		self.status.write("##########     Login DUT     ##########")
		self.status.write(" ")
		i = self.client.expect([ssh_newkey,"password:",pexpect.EOF])
		if i == 0:
			self.client.sendline('yes')
			i = self.client.p.expect([ssh_newkey,"password:",pexpect.EOF])
		if i == 1:
			self.client.sendline(password)
			self.client.expect(prompt)
			status.write(" ")
			status.write("##########     Login DUT Success     ##########")
			status.write(" ")
		if i == 2:
			status.write(" ")
			status.write("##########     Login DUT Failed     ##########")
			status.write("##########     Load SONiC Image failed     ##########")
			sys.exit()

	def load_SONiC_image_to_DUT(self):
		load_cmd = 'sudo sonic_installer install ' + self.image_url + ' -y'
		self.client.sendline(load_cmd)
		status.write("##########     Wait Max 300 seconds for Download & Load Image     ##########")
		self.client.expect(prompt,timeout=300)
		self.client.sendline('sudo reboot')



# print(console_server_ip + ':' + console_port)
# tn=telnetlib.Telnet(console_server_ip,console_port,10)  
# tn.set_debuglevel(2)

# ## This is Taipei Lab environment 
# tn.read_until('Login:'.encode()) 
# tn.write('administrator\r\n'.encode())
# tn.read_until('Password:'.encode()) 
# tn.write('password\r\n'.encode())

# print('Enter Console Server'.encode())
# tn.read_until('the Suspend Menu. \r\n'.encode()) 
# tn.write('\r\n'.encode())
# tn.write('\r\n'.encode())
# DUT_login = hostname+' login:'
# (x,y,z)=tn.expect([DUT_login.encode()],timeout=10)
# if x!=-1:
# 	tn.write('admin\r\n'.encode())
# 	tn.read_until('Password:'.encode())
# 	tn.write('YourPaSsWoRd\r\n'.encode())
# 	print('Enter SONiC')
# else:
# 	pass
# tn.read_until('$'.encode(),timeout=5)
# load_cmd = 'sudo sonic_installer install ' + image_url + ' -y \r\n'
# tn.write(load_cmd.encode())
# print('Load SONiC image')

# tn.read_until('$'.encode())
# tn.write('sudo reboot \r\n'.encode())
	
# (x,y,z)=tn.expect([DUT_login.encode()],timeout=300)
# if x!=-1:
# 	print('Reboot OK')
# 	tn.write('admin\r\n'.encode())
# 	tn.read_until('Password:'.encode())
# 	tn.write('YourPaSsWoRd\r\n'.encode())
# 	print('Enter SONiC')
# else:
# 	print('Reboot failed')
