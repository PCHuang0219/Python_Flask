import sys
sys.path.append("..")
from Config.get_all_config import *

org_log = sys.argv[1]
decode_log = sys.argv[2]
port = sys.argv[3]
port = port.replace('[','')
port = port.replace(']','')
port_list = []
while port != '' :
    port_pop = port.split(',')[0]
    port_list.append(port_pop)
    port = port.replace(port_pop+', ','')
    if port_pop == port :
        port = ''

f = open(org_log)
write_list = []
line_list = []
for line in f:
    for port in port :
        del_telnet='Telnet('+console_server_IP+','+port+'):'
        line=line.replace(del_telnet,'')
    if line[:5] != ' recv':
        pass
    else:
        line_list.append(line)
for line in line_list:
    line=line.replace(" recv b'",'')
    line=line.replace(r"\r\n",'\n')
    line=line.replace("'\n",'')
    line=line.replace("'",'')
    line=line.replace(r"\r",'')
    line=line.replace(r"\n",'')
    write_list.append(line)
    
with open(decode_log,"w") as file:
	for write_line in write_list:
		file.write(write_line)