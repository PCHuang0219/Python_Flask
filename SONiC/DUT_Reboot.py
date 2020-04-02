import telnetlib
import csv
import sys

model = sys.argv[1]

with open('./Config/DUT_Config.csv',newline='') as DUT_config:
    data = csv.DictReader(DUT_config)
    for row in data :
        if row['DUT_model'] == model:
            console_server_ip = row['console_server_ip']
			port = row['DUT_port']
            hostname = row['DUT_hostname']

tn=telnetlib.Telnet(console_server_ip,port,10)  
tn.set_debuglevel(2)
'''
tn.read_until('Login:'.encode()) 
tn.write('administrator\r\n'.encode())
tn.read_until('Password:'.encode()) 
tn.write('password\r\n'.encode())
'''
print('Enter Console Server'.encode())
tn.read_until('the Suspend Menu. \r\n'.encode()) 
tn.write('\r\n'.encode())
tn.write('\r\n'.encode())
DUT_login = hostname+' login:'
(x,y,z)=tn.expect([DUT_login.encode()],timeout=300)
if x!=-1:
	tn.write('admin\r\n'.encode())
	tn.read_until('Password:'.encode())
	tn.write('YourPaSsWoRd\r\n'.encode())
	print('Enter SONiC')
else:
	pass
tn.read_until('$'.encode(),timeout=5)
tn.write('sudo reboot \r\n'.encode())
print('Rebootg')

(x,y,z)=tn.expect([DUT_login.encode()],timeout=300)
if x!=-1:
	print('Reboot OK')
	tn.write('admin\r\n'.encode())
	tn.read_until('Password:'.encode())
	tn.write('YourPaSsWoRd\r\n'.encode())
	print('Enter SONiC')
else:
	print('Reboot failed')
