import sys
sys.path.append("..")
from Config.Get_All_Config import *
from Database.Update_Info import *
from collections import deque
import os
import codecs
import requests
import subprocess
import json

web_server = web_server_ip+':'+web_server_port

class Data_Base():
  def __init__(self):
    self.update = Update_Info()
  
  def get_job_information(self,job_id):
    return self.update.get_job_information(job_id)

  ### Bug need to fix
  # def get_testcases_list(self):
  #   execute_py = 'docker exec -i '+ docker_id + ' python3 /var/jlo/Ansible_Docker_Script/parse_testcases.py'
  #   copy_file = 'docker cp anber-test:/var/jlo/Ansible_Docker_Script/testcases.csv /home/jlo/Anber'
  #   p = subprocess.call(execute_py,shell=True,stdout=subprocess.PIPE)
  #   p = subprocess.call(copy_file,shell=True,stdout=subprocess.PIPE)
  #   csv_file = '/home/jlo/Anber/testcases.csv'
  #   testcases_list = []
  #   with open (csv_file, newline='') as csvfile :
  #     rows = csv.DictReader(csvfile)
  #     for row in rows :
  #       testcases_list.append([row["Test Case"],row["Test Name"],row["Topology"]])
  #   return testcases_list
    
  def get_status_log(self,job_id):
    log_list = []
    log_file = '/source/report/'+job_id+'/status.txt'
    log_path = '/source/report/'+job_id+'/'
    if not os.path.isdir(log_path):
      os.makedirs(log_path)
    cmd = "sshpass -p 1111 ssh root@10.100.43.132 'cat anber_sys_log' > " + log_file
    os.system(cmd)
    with open(log_file,'r') as logfile :
      lines = deque(logfile,80)
      for line in lines:
        log_list.append(line)
        line = line.replace('[0;31m','') 
        line = line.replace('[0;32m','')
        line = line.replace('[0;33m','')
        line = line.replace('[0;34m','')
        line = line.replace('[0;36m','')
        line = line.replace('[1;30m','')
        line = line.replace('[0m','')
        log_list.append(line)
    return log_list

  def get_org_log(self,job_id,case,topology):
    log_path = '/source/report/'+job_id+'/'
    log_file = log_path+case+'_'+topology+'_org_log.txt'
    log_list=[]
    try:
      f = codecs.open(log_file,encoding='utf-8')
      for log_line in f :
        log_list.append(log_line)
      return log_list
    except:
      return "Test Failed"
  
  def get_new_log(self,job_id,case,topology):
    log_path = '/source/report/'+job_id+"/"
    log_file = log_path+case+'_'+topology+'_log.txt'
    log_list=[]
    try:
      f = codecs.open(log_file,encoding='utf-8')
      for log_line in f :
        log_list.append(log_line)
      return log_list
    except:
      pass

  def sent_test_log(self,job_id,test_id,case,topology):
    if topology != "Minipack":
      detail_log = json.dumps(self.get_org_log(job_id,case,topology))
      brief_log = json.dumps(self.get_new_log(job_id,case,topology))
      r = requests.post('http://' + web_server + '/test/save/finishedTestLog/', \
        data = {'complete_log': detail_log ,'brief_log': brief_log ,'job_id': job_id ,'test_id':test_id } , verify = False)
    else:
      log_list = []
      log_file = '/source/report/'+job_id+'/'+'minipack_diag_log.txt'
      f = codecs.open(log_file,encoding='utf-8')
      for log_line in f:
        log_list.append(log_line)
      log_content = json.dumps(log_list)
      r = requests.post('http://' + web_server + '/test/save/finishedTestLog/', \
        data = {'complete_log': log_content ,'brief_log': log_content ,'job_id': job_id ,'test_id':test_id } , verify = False)

  def update_job_start_time(self,job_id,start_time):
    results = self.update.update_job_start_time(job_id,start_time)
    print("Update Job Start Time   " + str(results) )

  def update_job_end_time(self,job_id,end_time):
    results = self.update.update_job_end_time(job_id,end_time)
    print("Update Job End Time   " + str(results) )

  def update_job_status(self,job_id,status):
    results = self.update.update_job_status(job_id,status)
    print("Update Job Status   " + str(results) )

  def update_job_result(self,job_id,result):
    results = self.update.update_job_result(job_id,result)
    print("Update Job Result   " + str(results) )

  def update_current_testcase(self,job_id,testcasename):
    results = self.update.update_job_current_testcase(job_id,testcasename)
    print("Update Current Testcase Name   " + str(results) )

  def update_test_status(self,job_id,testcase_id,status):
    results = self.update.update_test_status(job_id,testcase_id,status)
    print("Update Testcase Status   " + str(results) )

  def update_test_result(self,job_id,testcase_id,result):
    results = self.update.update_test_result(job_id,testcase_id,result)
    print("Update Testcase Result   " + str(results) )

  def update_test_start_time(self,job_id,testcase_id,starttime):
    results = self.update.update_test_start_time(job_id,testcase_id,starttime)
    print("Update Testcase Start Time   " + str(results) )
  
  def update_test_end_time(self,job_id,testcase_id,endtime):
    results = self.update.update_test_end_time(job_id,testcase_id,endtime)
    print("Update Testcase End Time   " + str(results) )

  # def sent_test_detail_result(self,test):
  #   org_log = self.get_org_log(test.job_id,test.case,test.topology)
  #   new_log = self.get_new_log(test.job_id,test.case,test.topology)
  #   org_log = json.dumps(org_log)
  #   new_log = json.dumps(new_log)
  #   test.result = json.dumps(test.result)
  #   r = requests.post('http://'+web_server+'/test/server/testResult/', \
  #     data = {'job_id':test.job_id,'test_case':test.case,'test_name':test.name, \
  #     'test_topo':test.topology,'status':test.status,'result':test.result, \
  #     'start_time':test.start_time,'end_time':test.end_time,'complete_log':org_log,'summary_log':new_log} , verify = False )

  # def sent_test_information(self,test):
  #   r = requests.post('http://'+web_server+'/test/server/startTest/', \
  #     data = {'job_id':test.job_id,'test_case':test.case,'status':test.status, \
  #     'test_topo':test.topology,'start_time':test.start_time} , verify = False )
      
  #   if(r.status_code != requests.codes.ok):
  #     test.is_send = False
  #   else:
  #     test.is_send = True

  # def recovery_connect(self,job_id):
  #   for test in Job(job_id).finished_test_list:
  #     if(test.is_send == False):
  #       self.sent_test_information(test)

  # def sent_job_information(self,job):
  #   r = requests.post('http://'+web_server+'/test/server/startJob/', data = {'job_id':job.job_id, \
  #     'status':"running",'start_time':job.start_time} , verify = False )

  # def sent_job_result(self,job):
  #   r = requests.post('http://'+web_server+'/test/server/jobResult/', data = {'job_id':job.job_id, \
  #     'status':"finished",'start_time':job.start_time,"end_time":job.end_time,"result":"no result"} , verify = False )      