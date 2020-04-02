import sys
import subprocess
import time

model = sys.argv[1]
image_name = sys.argv[2]
test_name = sys.argv[3]
test_case = sys.argv[4]
port = sys.argv[5]
port = port.replace('[','')
port = port.replace(']','')
port_list = []
while port != '' :
    port_pop = port.split(',')[0]
    port_list.append(port_pop)
    port = port.replace(port_pop+', ','')
    if port_pop == port :
        port = ''
'''
if image_name != None :
    i = 0
    for a in range(len(port_list)):
        port = port_list[i].replace("'",'')
        hostname = hostname[i]
        Load_Image_To_DUT(port,hostname,image_name)
        i+=1
else :
'''
execute_testcase = test_name+test_case
'''
i = 0
for a in range(len(port_list)):
    port = port_list[i].replace("'",'')
    hostname = hostname[i]
    i+=1
    Copy_Test_Config(port,hostname,test_case,execute_testcase,i)
'''
p = subprocess.call(['python3','../SONiC/Testcase_Script/'+test_name+'/'+execute_testcase+'.py'])