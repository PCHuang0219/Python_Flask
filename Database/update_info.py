#!/usr/bin/python3
"""
Module Name: update_info.py
Purpose: To convert format to JSON and modify the value in the database.

Description:
    To convert format to JSON and modify the value in the database.
History:
    Anber Huang 06/30/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

import sys
sys.path.append("..")
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from Database.update_db import Update_DB

class Update_Info(Update_DB):
    def __init__(self):
        self._database = super().__init__()

    def update_job_status(self,job_id,content):
        return self.update_job(job_id,"status",content)

    def update_job_result(self,job_id,content):
        return self.update_job(job_id,"result",content)

    def update_job_start_time(self,job_id,content):
        return self.update_job(job_id,"start_time",content)

    def update_job_end_time(self,job_id,content):
        return self.update_job(job_id,"end_time",content)

    def update_job_current_testcase(self,job_id,content):
        return self.update_job(job_id,"running_test_id",content)

    def update_test_start_time(self,job_id,test_id,content):
        return self.update_test_content_list(job_id,test_id,"test_start_time",content)

    def update_test_end_time(self,job_id,test_id,content):
        return self.update_test_content_list(job_id,test_id,"test_end_time",content)

    def update_test_status(self,job_id,test_id,content):
        return self.update_test(job_id,test_id,"test_status",content)

    def update_test_result(self,job_id,test_id,content):
        return self.update_test_content_list(job_id,test_id,"test_result",content)

    def update_test_case_id(self, job_id, test_id, content):
        return self.update_test(job_id,test_id,"test_case_id",content)

    def init_test(self, job_id):
        init_list = []
        self.update_job(job_id, 'test_report_url', '')
        self.update_job(job_id, 'CPU_usage_rate', init_list)
        test_list = self.get_job_information(job_id)["testcase_list"]
        for test in test_list:
            test_id = test["test_id"]
            self.update_test_status(job_id, test_id, 'not start')
            self.update_test_content_list(job_id, test_id, "test_start_time", "", init=True)
            self.update_test_content_list(job_id, test_id, "test_end_time", "", init=True)
            self.update_test_content_list(job_id, test_id, "test_result", "", init=True)
            self.update_test_content_list(job_id, test_id, "test_during_time", "", init=True)

    def calculateDuringTime(self, job_id, test_id):
        test_case = self._database.find({"_id":ObjectId(job_id)},{"testcase_list":1,"_id":0})[0]['testcase_list']
        start = datetime.strptime(test_case[test_id]['test_start_time'][-1], '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(test_case[test_id]['test_end_time'][-1],  '%Y-%m-%d %H:%M:%S')
        during = end - start
        self.update_test_content_list(job_id, test_id, 'test_during_time', str(during))

    def get_job_information(self, job_id):
        job = self._database.find_one(ObjectId(job_id))
        return job
 
    def updateCPUUsageRate(self, job_id, time, rate):
        value = dict(time=time, rate=rate)
        result = self._database.find_one({'_id': ObjectId(job_id), 'CPU_usage_rate':{"$exists": True}}, {'_id':0, 'CPU_usage_rate':1})
        if result == None:
            value_list = []
            value_list.append(value)
            self.update_job(job_id, 'CPU_usage_rate', value_list)
        else:
            value_list = result['CPU_usage_rate']
            value_list.append(value)
            self.update_job(job_id, 'CPU_usage_rate', value_list)