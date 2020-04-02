#!/usr/bin/python3
"""
Module Name: database.py
Purpose: To communicate with front-end and database (MongoDB).

Description:
    This module mainly sends log and report to front-end and catches or modifies the value in the database.
History:
    Anber Huang 06/30/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

import sys
sys.path.append("..")
from Config.get_all_config import *
from Database.update_info import *
from collections import deque
from datetime import datetime
import os
import time
import codecs
import requests
import subprocess
import json
import random
import chart_studio.plotly as py
from plotly.figure_factory import create_gantt
import plotly
import traceback
import matplotlib.pyplot as plt

web_server = web_server_ip+':'+web_server_port

class Data_Base():
  def __init__(self):
    self.update = Update_Info()

  def get_job_information(self,job_id):
    return self.update.get_job_information(job_id)

  def setJobResultByJobID(self, job_id):
    self.update.setJobResultByJobID(job_id)

  def getJobStatusByJobID(self, job_id):
    return self.update.getJobstatusByJobID(job_id)

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

  def get_status_log(self,job_id,platform):
    log_list = []
    log_file = '../../report/'+job_id+'/status.txt'
    log_path = '../../report/'+job_id+'/'
    if not os.path.exists(log_path):
      os.makedirs(log_path)
    with open(log_file,'r') as logfile :
      lines = deque(logfile,80)
      for line in lines:
        line = line.replace('[0;31m','')
        line = line.replace('[0;32m','')
        line = line.replace('[0;33m','')
        line = line.replace('[0;34m','')
        line = line.replace('[0;36m','')
        line = line.replace('[1;30m','')
        line = line.replace('[0m','')
        line = line.replace(' ','&nbsp; ')
        log_list.append(line)
    return log_list

  def get_org_log(self,job_id,case,topology):
    log_path = '../../report/'+job_id+'/'
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
    log_path = '../../report/'+job_id+"/"
    log_file = log_path+case+'_'+topology+'_log.txt'
    log_list=[]
    try:
      f = codecs.open(log_file,encoding='utf-8')
      for log_line in f :
        log_list.append(log_line)
      return log_list
    except:
      pass

  def sent_test_log(self,job_id,test_id,case,topology,diag_item=''):
    if topology != "":
      detail_log = json.dumps(self.get_org_log(job_id,case,topology))
      brief_log = json.dumps(self.get_new_log(job_id,case,topology))
      r = requests.post('http://' + web_server + '/test/save/finishedTestLog/', \
        data = {'complete_log': detail_log ,'brief_log': brief_log ,'job_id': job_id ,'test_id':test_id } , verify = False)
    else :
      log_list = []
      if diag_item != '':
        log_file = '../../report/'+job_id+'/'+'PASS - diag_' + diag_item + '.log'
        if os.path.isfile(log_file) == False :
          log_file = '../../report/'+job_id+'/'+'FAIL - diag_' + diag_item + '.log'
      else:
        log_file = '../../report/'+job_id+'/'+'PASS - ' + TEST_CASES_DICT[case][1] + '.log'
        if os.path.isfile(log_file) == False :
          log_file = '../../report/'+job_id+'/'+'FAIL - ' + TEST_CASES_DICT[case][1] + '.log'
          if os.path.isfile(log_file) == False :
            log_file = '../../report/'+job_id+'/'+'EXCEPTION - ' + TEST_CASES_DICT[case][1] + '.log'
      f = codecs.open(log_file,encoding='utf-8')
      for log_line in f:
        log_list.append(log_line)
      log_content = json.dumps(log_list)
      r = requests.post('http://' + web_server + '/test/save/finishedTestLog/', \
        data = {'complete_log': log_content ,'brief_log': log_content ,'job_id': job_id ,'test_id':test_id } , verify = False)

  def update_job_start_time(self,job_id,start_time):
    self.update.update_job_start_time(job_id,start_time)

  def update_job_end_time(self,job_id,end_time):
    self.update.update_job_end_time(job_id,end_time)

  def update_job_status(self,job_id,status):
    self.update.update_job_status(job_id,status)

  def update_job_result(self,job_id,result):
    self.update.update_job_result(job_id,result)

  def update_current_testcase(self,job_id,testcasename):
    self.update.update_job_current_testcase(job_id,testcasename)

  def update_test_case_id(self, job_id, test_id, test_case_id):
    self.update.update_test_case_id(job_id, test_id, test_case_id)

  def update_test_status(self,job_id, test_case_id,status):
    self.update.update_test_status(job_id, test_case_id,status)

  def update_test_result(self,job_id, test_case_id,result):
    self.update.update_test_result(job_id, test_case_id,result)

  def update_test_start_time(self,job_id, test_case_id,starttime):
    self.update.update_test_start_time(job_id, test_case_id,starttime)

  def update_test_end_time(self,job_id, test_case_id,endtime):
    self.update.update_test_end_time(job_id, test_case_id,endtime)
    if endtime != "Running":
      self.update.calculateDuringTime(job_id, test_case_id)

  def randomColor(self):
      colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
      color = ""
      for i in range(6):
          color += colorArr[random.randint(0,14)]
      return "#"+color

  def generateWordReport(self, job_id):
    try:
      script_name = '../Execute/' + job_id + '_report.py'
      init_script = open('../Execute/auto_report.init', 'r')
      script = open(script_name, 'w')
      script.write(init_script.read() + '\n\n')

      job_info = self.update.get_job_information(job_id)
      cpu_line_rate_file = self.generateCPUUsageRateLineChart(job_info)
      FMT = '%Y-%m-%d %H:%M:%S'
      start = datetime.strptime(job_info['start_time'], FMT)
      end = datetime.strptime(job_info['end_time'],  FMT)
      job_during_time = str(end - start)
      modifyJobCLI = "modifyJobInfo('"
      modifyJobCLI += job_info['project']      + "', '"
      modifyJobCLI += job_info['job_name']     + "', '"
      modifyJobCLI += job_info['job_describe'] + "', '"
      modifyJobCLI += job_info['start_time']   + "', '"
      modifyJobCLI += job_info['end_time']     + "', '"
      modifyJobCLI += job_during_time  + "', '"
      web_link = 'http://' + web_server + '/test/jobManagement/jobDetail/?jobId=' + job_id
      gantt_link = 'http://' + web_server_ip + ':8888/log/' + job_id + '/gantt.html'
      modifyJobCLI += web_link + "', '"
      modifyJobCLI += gantt_link + "', '"
      modifyJobCLI += job_info['status'] + "', '"
      modifyJobCLI += job_info['result'] + "', "
      modifyJobCLI += str(len(job_info['testcase_list'])) + ")"
      script.writelines(modifyJobCLI + '\n\n')

      pre_stage_no = ""
      pre_thread_no = ""
      summaryCLI = ""
      detailCLI = ""
      df = []
      colors = []
      index = 0
      for test_case in job_info['testcase_list']:
        try:
          stage_no = test_case['test_stage_id']
        except:
          stage_no = 1
        if pre_stage_no != stage_no:
          pre_stage_no = stage_no
          colors.append(self.randomColor())
          cli = 'addStageTitle(' + str(stage_no) +')\n'
          summaryCLI += cli
          detailCLI += cli

        thread_no = test_case['test_thread_id']
        if pre_thread_no != thread_no:
          pre_thread_no = thread_no
          start_time = str(test_case['test_start_time'][0])
          time_format = '%Y-%m-%d %H:%M:%S'
          end_time = time.strptime(start_time, time_format)
          for test in job_info['testcase_list']:
            if test['test_thread_id'] == pre_thread_no:
              compare_time = time.strptime(test['test_end_time'][-1], time_format)
              end_time = compare_time if compare_time > end_time else end_time
          end_time = time.strftime(time_format, end_time)
          index = 0
          cli = 'addThreadTitle(' + str(thread_no) + ', "' + start_time + '", "' + end_time + '")\n'
          summaryCLI += cli 
          detailCLI += cli

          df.append(dict(Index='Stage_ID:%s' % stage_no, Start=start_time, Finish=end_time, Task='Thread_ID:%d' % thread_no))

        total = len(test_case['test_result'])
        times_of_pass = test_case['test_result'].count('Success')
        if isinstance(test_case['test_during_time'],list):
          total_times = float()
          times = 0
          FMT = '%H:%M:%S'
          time_list = test_case['test_during_time']
          for during_time in time_list:
            a = time.strptime(during_time,FMT)
            b = timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).total_seconds()
            total_times += b
            times += 1
          average_time = timedelta(seconds=(total_times / times))
        else:
          average_time = test_case['test_during_time']

        addTestInfoCLI = "addTestCaseInfo('"
        addTestInfoCLI += job_id                             + "', "
        addTestInfoCLI += str(test_case['test_id'])          + ", '"
        addTestInfoCLI += str(test_case['test_case_id'])     + "', u'"
        addTestInfoCLI += test_case['test_name']             + "', u'"
        addTestInfoCLI += test_case['test_case']             + "', '"
        addTestInfoCLI += test_case['test_status']           + "', "
        addTestInfoCLI += str(total)                         + ", "
        addTestInfoCLI += str(times_of_pass)                 + ", '"
        addTestInfoCLI += str(average_time)                  + "', '"
        addTestInfoCLI += str(index)                         + "')\n"
        detailCLI += addTestInfoCLI
        index += 1

      save_CLI = "doc.save('../../report/" + job_id + "/" + job_id + "_report.docx')"
      add_picure = "addPicture('" + cpu_line_rate_file + "')\n"
      script.writelines(summaryCLI)
      script.writelines(detailCLI)
      script.writelines(add_picure)
      script.writelines(save_CLI)
      script.close()
      self.generateGanttChartToDisplayWorkflow(job_info, df, colors)
      subprocess.call('python ' + script_name, shell=True, stderr=subprocess.PIPE)
      os.remove(script_name)
      self.sendWordReportToWebServer(job_id)
    except Exception as e:
      error_class = e.__class__.__name__ #取得錯誤類型
      detail = e.args[0] #取得詳細內容
      cl, exc, tb = sys.exc_info() #取得Call Stack
      lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
      fileName = lastCallStack[0] #取得發生的檔案名稱
      lineNum = lastCallStack[1] #取得發生的行號
      funcName = lastCallStack[2] #取得發生的函數名稱
      print("File         " + fileName)
      print("line         " + str(lineNum))
      print("funcName     " + funcName)
      print("error_class  " + error_class)
      print("detail       " + detail)
      os.remove(script_name)

  def generateGanttChartToDisplayWorkflow(self, job_info, df, colors):
    job_id = str(job_info['_id'])
    fig = create_gantt(df, colors=colors, index_col='Index', show_colorbar=True, group_tasks=True, title=job_info['job_name'] + ' Gantt Chart')
    # py.iplot(fig, filename='gantt-simple-gantt-chart', world_readable=True) 
    plotly.offline.plot(fig, filename='../../report/' + job_id + '/gantt.html', auto_open=False)

  def generateCPUUsageRateLineChart(self, job_info):
    job_id = str(job_info['_id'])
    file_name = '../../report/' + job_id + '/cpu_usage_rate.png'
    try:
      cpu_usage_rate_list = job_info['CPU_usage_rate']
    except:
      cpu_usage_rate_list = []
    time_list = []
    y = []
    for data in cpu_usage_rate_list:
      time_list.append(data['time'].split()[1])
      y.append(float(data['rate']))

    x = range(len(time_list))
    plt.plot(x, y, marker='o', mec='r', mfc='w',label='y=CPU Usage Rate')
    plt.tick_params(labelsize=8)
    plt.legend()
    plt.xticks(x, time_list, rotation=45)
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel("time")
    plt.ylabel("CPU Usage Rate")
    plt.title("Facebook Minipack SIT CPU Usage Rate")
    plt.savefig(file_name, dpi=300)
    return file_name

  def sendWordReportToWebServer(self, job_id):
    file_name = '../../report/' + job_id + '/' + job_id + '_report.docx'
    gantt_name = '../../report/' + job_id + '/gantt.html'
    f = open(file_name, 'rb')
    f1 = open(gantt_name, 'rb')
    files = {'report': f, 'gantt':f1}
    r = requests.post('http://' + web_server + '/test/save/finishedTestReport/', \
        files=files, data={'job_id':job_id})

  def insertCPUUsageRate(self, job_id, time, rate):
    self.update.updateCPUUsageRate(job_id, time, rate)

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