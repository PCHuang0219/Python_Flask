import sys
sys.path.append("..")
from Config.get_all_config import *
import subprocess
import linecache
import codecs
import os

def Ansible_Run(job_id,TESTCASE,TESTNAME,TOPONAME):
    current_path = str(os.getcwd())
    current_path = current_path.replace("Execute","SONiC/")
    try:
        os.makedirs('/source/report/'+job_id)
    except :
        pass
    status_file='/source/report/'+job_id+'/status.txt'
    status=open(status_file,'a')
    line_list = []
    CH_file=current_path+"Ansible_Auto_Script_Org.sh"
    RUN_file=current_path+"Ansible_Auto_Script_Run.sh"

    CH_copy=linecache.getline(CH_file,9)
    CH_chmod=linecache.getline(CH_file,10)
    CH_RMTOPO=linecache.getline(CH_file,15)
    CH_TOPO=linecache.getline(CH_file,15)
    CH_VERIFY=linecache.getline(CH_file,19)
    CH_TEST=linecache.getline(CH_file,21)

    f = codecs.open(CH_file,encoding='utf-8')
    line_num = 0
    for line in f:
        line_num += 1
        # Start docker sonic-mgmt
        if line_num == 7 :
            line_list.append("docker start "+docker_name)
        # Copy ansible test shell script to docker container and +X for flask server
        elif line_num == 9 :
            line_list.append("docker cp "+current_path+"Ansible_Docker_Script "+docker_id+":/var/"+docker_username)
        elif line_num == 10 :
            line_list.append("docker exec -i "+docker_id+" sudo chmod 777 -R Ansible_Docker_Script")
        # Remove All Topology        
        # elif line_num == 12 :
        #     line_list.append("docker exec -i "+docker_id+" sh /var/"+docker_username+"/Ansible_Docker_Script/ansible_remove_topology.sh")
        # Add Test Topology
        elif line_num == 15 :
            line_list.append("docker exec -i "+docker_id+" sh /var/"+docker_username+"/Ansible_Docker_Script/ansible_add_topology.sh "+TOPONAME)
        # Reboot DUT and verify DUT on test topology
        elif line_num == 17 :
            line_list.append("docker exec -i "+docker_id+" sh /var/"+docker_username+"/Ansible_Docker_Script/ansible_verify_DUT.sh "+TOPONAME)
        # Testcase
        elif line_num == 19 :
            line_list.append("docker exec -i "+docker_id+" sh /var/"+docker_username+"/Ansible_Docker_Script/ansible_run_testcase.sh "+TOPONAME+" "+TESTNAME+" | tee /source/report/"+job_id+"/"+TESTCASE+"_"+TOPONAME+"_org_log.txt")
        else:
            line_list.append(line)

    with open(RUN_file,"w") as file:
        for write_line in line_list:
            file.write(write_line+'\n')
    try:
        p = subprocess.call("sh "+RUN_file,shell=True,stdout=status,stderr=subprocess.PIPE)
        return "Success"
    except subprocess.CalledProcessError as e:
        print("Test error returncode: " + e.returncode)
        return "Error"

def Ansible_Log(job_id,TESTCASE,TOPONAME):
    log_file="/source/report/"+job_id+"/"+TESTCASE+"_"+TOPONAME+"_org_log.txt"
    f = open(log_file,'r')
    line_list = []
    error_list = []
    i=0
    j=0
    for line in f :
        RESULT=line[:10]
        i+=1
        if RESULT =="PLAY RECAP":
            j=i
        else:
            pass
        a = line.find("FAILED!")
        if a>0 :
            line = line.replace('[0;31m','') 
            line = line.replace('[0m','')
            error_list.append(str (i)+'   '+line)
            i = int (i)
        else:
            pass
    line_list.append("***************************    TASK    "+TESTCASE+"    ***************************")

    line = linecache.getline(log_file,j+3)
    p = line.find('+')
    i = line.find('*')
    line_list.append("END_TIME:   "+line[:p-1]+"     "+"EXECUTION_TIME:   "+line[i-12:i])

    result = linecache.getline(log_file,j+1)
    result = result.replace('[0;31m','') 
    result = result.replace('[0;32m','')
    result = result.replace('[0;33m','')
    result = result.replace('[0m','')
    line_list.append(result)

    line_list.append("***************************************************************************")

    if os.path.exists('/source/report/'+job_id):
        os.makedirs('/source/report/'+job_id)
    new_log_path = '/source/report/'+job_id+'/'
    new_log_file = new_log_path+TESTCASE+"_"+TOPONAME+"_log.txt"
    with open(new_log_file,"w") as file:
        for write_line in line_list:
            file.write(write_line+"\n")
        for write_line in error_list:
            file.write(write_line+"\n")

def Set_Ansible_Testcase_Result(job_id,TESTCASE,TOPONAME):
    log_path = '/source/report/'+job_id+'/'
    log_file = log_path+TESTCASE+"_"+TOPONAME+"_log.txt"
    f = open(log_file,'r')
    result = []
    line_number = 0
    ok_total = ''
    ch_total = ''
    un_total = ''
    fa_total = ''
    for line in f :
        line_number +=1
        if line_number == 3 :
            ok = line.find('ok=')
            ch = line.find('changed=')
            un = line.find('unreachable=')
            fa = line.find('failed=')
            ok_total = line[ok+3:ch].replace(' ','') 
            ch_total = line[ch+8:un].replace(' ','')
            un_total = line[un+12:fa].replace(' ','')
            fa_total = line[fa+7:-2].replace(' ','')
    
    result.append("OK="+ok_total)
    result.append("Changed="+ch_total)
    result.append("Unreachable="+un_total)
    result.append("Failed="+fa_total)
    ok_total = int (ok_total)
    ch_total = int (ch_total)
    un_total = int (un_total)    
    fa_total = int (fa_total)
    total = ok_total+ch_total+un_total+fa_total
    ## define test result
    if fa_total / total == 0.0 :
        result.append("Pass")
    elif fa_total / total < 1.0  :
        result.append("Failed")
    elif fa_total / total == 1.0 :
        result.append("Failed")
    return result