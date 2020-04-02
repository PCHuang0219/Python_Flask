#!/usr/bin/python3
"""
Module Name: job.py
Purpose: Job module

Description:
    This module is a set of multiple test cases selected by user providing class methods for storing job information 
    and multiple test cases class method, it can be used change the value in Database of TMS from python file in forlder named Database.
    It can define all test cases execution order by add_test method.
History:
    Anber Huang 06/30/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

import sys
sys.path.append("..")
from Execute.test_case import *
from Database.update_info import *
from Database.database import Data_Base
from Execute.time import *
from Config.get_all_config import *
import pexpect
import time
from threading import Thread

class Job():
    def __init__(self,job_id):
        self.database = Data_Base()
        self.job_name = ''
        self.job_id = job_id
        self.topo = ''
        self.model = ''
        self.platform = ''
        self.start_time = "It's not execute"
        self.end_time = "It's not execute"
        self.status = 'Wait'
        self.result = ''
        self.stage_list = []
        self.now_execute_test = None
        self.time=Time()
        self.image_version = 'None'
        self.previous_topology = 'All'
        self.stop_event = False

    def set_information(self, topo, model, platform, name, image):
        self.topo=topo
        self.model=model
        self.platform=platform
        self.job_name=name
        self.image_version = image

    def set_start_status(self):
        self.start_time = self.time.get_time_now()
        self.status = "Active"
        self.result = "Running"
        self.end_time = "Running"

    def set_end_status(self):
        self.end_time = self.time.get_time_now()
        self.status = "Finished"

    def update_current_testcase(self):
        self.database.update_current_testcase(self.job_id,self.now_execute_test.case_id)

    def get_job_status(self):
        return self.status       

    def get_new_test(self):
        self.now_execute_test = self.stage_list.pop(0)
        return self.now_execute_test

    def add_test(self,stage_list):
        for test_list in stage_list:
            test_case_list = []
            thread_list = []
            first_thread_id = test_list[0]['test_thread_id']
            for test_case in test_list:
                test=Test_Case()
                test.set_new_test(test_case,self.model,self.platform)
                if first_thread_id != test_case['test_thread_id']:
                    first_thread_id = test_case['test_thread_id']
                    thread_list.append(test_case_list)
                    test_case_list = [test]
                else:
                    test_case_list.append(test)

            thread_list.append(test_case_list)
            self.stage_list.append(thread_list)
    
    def execute_test_case(self):
        # Start executing job
        self.set_start_status()
        self.database.update.init_test(self.job_id)
        self.database.update_job_start_time(self.job_id,self.start_time)
        self.database.update_job_end_time(self.job_id,self.end_time)
        self.database.update_job_status(self.job_id,self.status)
        self.database.update_job_result(self.job_id,self.result)

        if self.platform == 'Facebook':
            t = Thread(target=self.getCPUUsageRate)
            t.start()
        # For loop to run testcase
        myThreads = []
        for stage in self.stage_list :
            for thread in stage:
                t = Thread(target=self.execute_test_from_test_list, args=(thread,))
                t.start()
                myThreads.append(t)

            for t in myThreads:
                if t.is_alive():
                    t.join()

        job_status = self.database.getJobStatusByJobID(self.job_id)['status']
        while job_status != 'Finished':
            time.sleep(1)
            self.database.setJobResultByJobID(self.job_id)
            job_status = self.database.getJobStatusByJobID(self.job_id)['status']

        # Set job finised and update job information to database.
        self.stop_event = True
        self.now_execute_test= None
        self.set_end_status()
        self.database.update_job_status(self.job_id,self.status)
        self.database.update_job_end_time(self.job_id,self.end_time)        
        self.database.generateWordReport(self.job_id)
    
    def execute_test_from_test_list(self, test_list):
        mode = test_list[0].execute_mode
        time_period_val = test_list[0].time_period
        if mode == 'cal_times':
            times = time_period_val
            while times > 0:
                for now_test in test_list:
                    now_test.set_status_running()
                    now_test.update_start_time()
                    now_test.update_status()
                    if self.platform == "SONiC":
                        if self.topo == "T_SONiC_Ansible" :
                            now_test.ansible_remove_topology(self.previous_topology)
                            now_test.execute_SONiC_Ansible(self.model,self.image_version)
                            self.previous_topology = now_test.topology
                        else :
                            now_test.execute_SONiC_non_Ansible(self.model,self.image_version)
                    elif self.platform == "Facebook":
                        now_test.execute_Facebook_test()
                    times -= 1 
        else:
            hours = time_period_val
            target_time = self.time.cal_target_time_from_now(hours)
            now_time = self.time.get_time_for_calculate()
            while now_time < target_time :
                for now_test in test_list:
                    now_time = self.time.get_time_for_calculate()
                    if now_time < target_time:
                        now_test.set_status_running()
                        now_test.update_start_time()
                        now_test.update_status()
                        if self.platform == "SONiC":
                            if self.topo == "T_SONiC_Ansible" :
                                now_test.ansible_remove_topology(self.previous_topology)
                                now_test.execute_SONiC_Ansible(self.model,self.image_version)
                                self.previous_topology = now_test.topology
                            else :
                                now_test.execute_SONiC_non_Ansible(self.model,self.image_version)
                        elif self.platform == "Facebook":
                            now_test.execute_Facebook_test()
                now_time = self.time.get_time_for_calculate()

    def getCPUUsageRate(self):
        while not self.stop_event:
            DUT_info = DUT_DICT[self.model]
            ssh_ip   = DUT_info['ssh_ip']
            ssh_port = DUT_info['ssh_port']
            username = DUT_info['username']
            password = DUT_info['password']
            prompt   = DUT_info['prompt']
            __dut = pexpect.spawn('ssh ' + username + '@' + ssh_ip + ' -p ' + ssh_port + ' -o StrictHostKeyChecking=no -o ServerAliveInterval=60', encoding='utf-8')
            __dut.expect('(?i)password.*')
            __dut.send(password + '\r')
            __dut.expect(prompt)
            __dut.send("top -n 1 | grep Cpu | awk {'print $2'}\r")
            __dut.expect(prompt)
            execute_time = self.time.get_time_now()
            usage_rate = __dut.before.splitlines()[1]
            __dut.close()
            self.database.insertCPUUsageRate(self.job_id, execute_time, usage_rate)
            time.sleep(300)

    ######## Redesign framework because web server can get data from mongo database, 2019/06/27 Anber_Huang
    ########
    # def get_percent_finish(self):
    #     remain_test_number = len(self.thread_list)
    #     finished_test_number = len(self.finished_test_list)
    #     if self.status == "Finish" :
    #         return '100'
    #     elif remain_test_number+finished_test_number == 0 :
    #         return '0'
    #     else :
    #         percent=(finished_test_number-1)/(remain_test_number+finished_test_number)*100
    #         return str(percent)

    # def get_running_time(self):
    #     if self.start_time_cal != None :
    #         if self.status == "Finish":
    #             return self.total_spand_time
    #         return str (self.time.get_time_for_calculate() - self.start_time_cal)
    #     return ''

    # def get_job_detail(self):
    #     all_detail=[]
    #     for finished_test in self.finished_test_list :
    #         all_detail.append({"test_name":finished_test.case + " - " +finished_test.topology, \
    #                         "test_status":finished_test.status, \
    #                         "test_result":finished_test.result, \
    #                         "start_time":finished_test.start_time, \
    #                         "end_time":finished_test.end_time})
    #     for undo_test in self.thread_list :
    #         all_detail.append({"test_name":undo_test.case + " - " + undo_test.topology, \
    #                         "test_status":undo_test.status, \
    #                         "test_result":undo_test.result, \
    #                         "start_time":undo_test.start_time, \
    #                         "end_time":undo_test.end_time})
    #     return all_detail

    # def get_remain_list_length(self):
    #     return len(self.thread_list)

    # def get_last50_lines(self):
    #     if (self.now_execute_test == None):
    #         return []
    #     return self.now_execute_test.get_last50_lines(self.job_id)
    
    # def get_test_running_name(self):
    #     if self.status == "Finish":
    #         return "Job is finished"
    #     elif self.now_execute_test == None:
    #         print("bbbb")
    #         return "None"
    #     else :
    #         print("get test"+self.now_execute_test.name)
    #         return self.now_execute_test.name