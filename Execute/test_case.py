#!/usr/bin/python3
"""
Module Name: test_case.py
Purpose: Testcase module

Description:
    This module is one of testcases selected by user providing class methods for storing test case information 
    and testing it automatically, you can change the value in Database of TMS from python file in forlder named Database.
    It also can define how to perform the automatic testing according different platforms or projects through "def" method.
History:
    Anber Huang 06/30/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

import sys
sys.path.append("..")
from Execute.time import *
from Database.database import *
from SONiC.Ansible_Test_Case import *
from Config.get_all_config import *
import subprocess
import os
import csv
import time

class Test_Case():
    def __init__(self):
        self.database = Data_Base()
        self.status = ""
        self.result = 'Not Start'
        self.start_time = "It's not execute"
        self.end_time = "It's not finish"
        self.time = Time()

    def createStatusFile(self):
        job_file = '../../report/'+self.job_id 
        try:
            os.makedirs(job_file)
        except:
            pass
        status_file = job_file + '/status.txt'
        self.status_file = open(status_file,'a')

    def ansible_remove_topology(self,topology='All'):
        if topology == 'All':
            cmd = 'docker exec -i ' + docker_id + ' sh /var/' + docker_username + '/Ansible_Docker_Script/ansible_remove_topology.sh'
        elif topology == 'vms-t0':
            cmd = 'docker exec -i ' + docker_id + ' sh /var/' + docker_username + '/Ansible_Docker_Script/ansible_remove_t0.sh'
        elif topology == 'vms-t1':
            cmd = 'docker exec -i ' + docker_id + ' sh /var/' + docker_username + '/Ansible_Docker_Script/ansible_remove_t1.sh'
        elif topology == 'vms-t1-lag':
            cmd = 'docker exec -i ' + docker_id + ' sh /var/' + docker_username + '/Ansible_Docker_Script/ansible_remove_t1-lag.sh'
        elif topology == 'ptf1-32':
            cmd = 'docker exec -i ' + docker_id + ' sh /var/' + docker_username + '/Ansible_Docker_Script/ansible_remove_ptf32.sh'
        p = subprocess.call(cmd,shell=True,stdout=self.status_file,stderr=subprocess.PIPE)
            
    def upgrade_SONiC_image(self,model,image_version):
        for model_info in model_list :
            if model_info['Model'] == model:
                DUT_hostname = model_info['Hostname']
        print("Upgrade DUT")
        image_url = 'http://210.63.221.19:8080/job/' + image_version + '/artifact/target/sonic-broadcom.bin'
        cmd = 'docker exec -i '+ docker_id + ' sh /var/jlo/Ansible_Docker_Script/ansible_upgrade_image.sh '+ DUT_hostname + ' ' + image_url
        p = subprocess.call(cmd,shell=True,stdout=self.status_file,stderr=subprocess.PIPE)

    def execute_SONiC_Ansible(self,model,image_version):
        if image_version != 'None':
            self.upgrade_SONiC_image(model,image_version)
        result = Ansible_Run(self.job_id,self.case,self.name,self.topology)
        if result == "Success" :
            Ansible_Log(self.job_id,self.case,self.topology)
            self.result = Set_Ansible_Testcase_Result(self.job_id,self.case,self.topology)
        else:
            self.result = "Failed"

        self.setStatusAfterTesting()

        self.database.sent_test_log(self.job_id,self.case_id,self.case,self.topology)
        print(self.time.get_time_now()+"          ansible_execute  OKOKOK")

    def execute_SONiC_non_Ansible(self,model,image_version):
        ## No Test Plan can convert auto test 
        # with open('../Config/DUT_Config.csv',newline='') as DUT_Config:
        #     data = csv.DictReader(DUT_Config)
        #     port = []
        #     hostname = []
        #     for row in data :
        #         if row['DUT_model'] == model:
        #             port.append(row['DUT_port'])
        #             hostname.append(row['DUT_hostname'])
        # if not os.path.exists('../../report/'+self.job_id):
        #     os.makedirs('../../report/'+self.job_id)
        # status_file = '../../report/'+self.job_id+'/status.txt'
        # org_log_file = '../../report/'+self.job_id+'/'+self.name+self.case+'_org.txt'
        # decode_log_file = '../../report/'+self.job_id+'/'+self.name+self.case+'.txt'
        # status=open(status_file,'a')
        # self.database.sent_test_log(self.job_id,self.case_id,self.case,self.topology)
        # print(self.time.get_time_now()+"          non_ansible_execute  OKOKOK")
        return "Failed"

    def execute_Facebook_test(self):
        vars_count = 0
        if self.name == "DIAG" or self.name == 'DIAG – Stress':
            vars_count = 3

        if self.case == "Monitor PDU":
            script_name = self.generateMainFileToExecute(vars_count ,pdu_requirement=True)
        else:
            script_name = self.generateMainFileToExecute(vars_count)

        if self.name == "DIAG" or self.name == 'DIAG – Stress':
            print("* * * * " + self.case + '    Start. * * * * * ')
            item_int, item_type = self.getFBDiagArgvs()
            p = subprocess.call('python3 ../Execute/' + script_name + '.py ' + item_int + ' ' + item_type + ' ' + self.case.replace(' ','_'), 
                                shell=True, stdout=self.status_file, stderr=sys.stdout)

            log_file = '../../report/'+self.job_id+'/'+'PASS - diag_' + item_int + '.log'
            if os.path.isfile(log_file) :
                self.result = 'Success'
            else:
                self.result = 'Failed'
            
            os.system('rm ../Execute/' + script_name + '.py')
            print("* * * * " + self.case + '    Finished. * * * * * ')
        else:
            print("* * * * " + self.case + '    Start. * * * * * ')
            p = subprocess.call('python3 ../Execute/' + script_name + '.py', 
                                shell=True, stdout=self.status_file, stderr=sys.stdout)
            
            item_int = ''
            log_file = '../../report/'+self.job_id+'/'+'PASS - ' + TEST_CASES_DICT[self.case][1] + '.log'
            if os.path.isfile(log_file) :
                self.result = 'Success'
            else:
                self.result = 'Failed'

            os.system('rm ../Execute/' + script_name + '.py')
            print("* * * * " + self.case + '    Finished. * * * * * ')

        self.setStatusAfterTesting()

        self.database.sent_test_log(self.job_id,self.case_id,self.case,self.topology,item_int)

    def getFBDiagArgvs(self):
        item_int = TEST_CASES_DICT[self.case][0]
        item_type = TEST_CASES_DICT[self.case][2]

        return item_int , item_type

    def generateMainFileToExecute(self ,vars_count ,pdu_requirement = False):
        import_class = TEST_CASES_DICT[self.case][1]
        initial_main = open("../Execute/main.init","r")
        script_name = self.case.replace(' ','_')
        script_name = script_name.replace('/','_')
        main_file = open("../Execute/" + script_name + ".py","w")
        main_file.write(initial_main.read())

        main_file.writelines("# Import the test script\r\n") # Import the test script
        import_cli = "from " + self.platform + "." + import_class.lower() + " import " + import_class + "\r\n"
        main_file.writelines(import_cli) 

        main_file.writelines("# Initialize and run script.\r\n")# Initialize and run script.
        main_file.writelines("COMe = settings.Minipack_COMe()\r\n")
        main_file.writelines("BMC = settings.Minipack_BMC()\r\n")
        main_file.writelines("dut = [COMe, BMC]\r\n")
        if pdu_requirement == True:
            main_file.writelines("pdu = settings.ATEN_PDU()\r\n")
        for i in range(0,vars_count + 1):
            if i == 0 :
                if pdu_requirement == True:
                    parameter = "(dut, pdu"
                else:
                    parameter = "(dut"
            else:
                parameter += ", argv" + str(i)
        parameter += ", job_id='" + self.job_id + "')"
        main_file.writelines("testcase = " + import_class + parameter + "\r\n")
        main_file.writelines("try:\r\n")
        main_file.writelines("  testcase.run()\r\n")
        main_file.writelines("  testcase.stop()\r\n")
        main_file.writelines("except Exception as e:\r\n")
        main_file.writelines("  UI.log('RAISE EXCEPTION', str(e))\r\n")
        main_file.writelines("  error_class = e.__class__.__name__ #取得錯誤類型\r\n")
        main_file.writelines("  detail = e.args[0] #取得詳細內容\r\n")
        main_file.writelines("  cl, exc, tb = sys.exc_info() #取得Call Stack\r\n")
        main_file.writelines("  lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料\r\n")
        main_file.writelines("  fileName = lastCallStack[0] #取得發生的檔案名稱\r\n")
        main_file.writelines("  lineNum = lastCallStack[1] #取得發生的行號\r\n")
        main_file.writelines("  funcName = lastCallStack[2] #取得發生的函數名稱\r\n")
        main_file.writelines('  print("File         " + fileName)\r\n')
        main_file.writelines('  print("line         " + str(lineNum))\r\n')
        main_file.writelines('  print("funcName     " + funcName)\r\n')
        main_file.writelines('  print("error_class  " + error_class)\r\n')
        main_file.writelines('  print("detail       " + detail)\r\n')
        main_file.writelines("  UI.test_result = 'EXCEPTION'\r\n")
        main_file.writelines("  testcase.stop()\r\n")
        main_file.close()
        return script_name

    def set_new_test(self,test_info, model, platform):
        self.job_id = test_info["job_id"]
        self.name = test_info["test_name"]
        self.case = test_info["test_case"]
        self.topology = test_info["test_topo"]
        self.case_id = test_info["test_id"]
        self.model = model
        self.platform = platform
        self.thread_id = test_info["test_thread_id"]
        try:
            self.stage_id = test_info["test_stage_id"]
        except:
            self.stage_id = '0'
        try:
            self.time_period = test_info["test_time_period"]
            if self.time_period.split(" ")[1] == "times":
                self.execute_mode = "cal_times"
                self.time_period = int(self.time_period.split(" ")[0])
            else:
                self.execute_mode = "hours"
                self.time_period = self.time_period.split(" ")[0]
        except:
            self.execute_mode = "cal_times"
            self.time_period = 1

        self.createStatusFile()

    def setStatusAfterTesting(self):
        # set status to finish
        self.status = "Finished"
        self.end_time = self.time.get_time_now()

        # update status
        self.update_status()
        self.database.update_test_case_id(self.job_id, self.case_id, TEST_CASES_DICT[self.case][0])

        self.database.setJobResultByJobID(self.job_id)

    def set_status_running(self):
        self.start_time = self.time.get_time_now()    
        self.status = "Running"
        self.result = "Running"
        self.end_time = "Running"

    def update_start_time(self):
        self.database.update_test_start_time(self.job_id,self.case_id,self.start_time)
    
    def update_status(self):
        self.database.update_test_status(self.job_id,self.case_id,self.status)

        # update result
        self.database.update_test_result(self.job_id,self.case_id,self.result)
        # update end time
        self.database.update_test_end_time(self.job_id,self.case_id,self.end_time)