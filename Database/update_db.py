#!/usr/bin/python3
"""
Module Name: update_db.py
Purpose: To modify the value in MongoDB.

Description:
    This module mainly modifies the value under the table named "job_info" in database named "job" .
History:
    Anber Huang 06/30/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

import sys
sys.path.append("..")
from Database.mongo_db import *
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import time

class Update_DB():
    def __init__(self):
        self._database = database.get_collection("job_info")
        return self._database

    def update_job(self, job_id, value, key):
        condition = {"_id":ObjectId(job_id)}
        job = self._database.find_one(condition)
        job[value] = key
        result = self._database.update(condition,job)
        return result

    def update_test(self, job_id, test_id, key, value):
        condition = { "_id":ObjectId(job_id),"testcase_list.test_id":int(test_id)}
        modify_value = "testcase_list.$." + key
        content = { '$set' : { modify_value : value }}
        result = self._database.update(condition,content)
        return result

    def update_test_content_list(self, job_id, test_id, key, value, init=False):
        test_case = self._database.find_one({'_id':ObjectId(job_id)}, {'testcase_list':1, '_id':0})['testcase_list'][test_id]
        orgVal = test_case[key]
        if not init: 
            if not isinstance(orgVal, list):
                orgVal = [orgVal]
            if len(orgVal) > 0:
                val = orgVal[-1]
                if val == 'NULL' or val == 'Running' or val == 'not finished':
                    orgVal.pop(-1)
                if val != value:
                    orgVal.append(value)
                else:
                    return "No change"
            else:
                orgVal.append(value)
        else:
            orgVal = []    

        return self.update_test(job_id, test_id, key, orgVal)

    # def calculateDuringTime(self, job_id, test_id):
    #     test_case = self._database.find({"_id":ObjectId(job_id)},{"testcase_list":1,"_id":0})[0]['testcase_list']
    #     start = datetime.strptime(test_case[test_id]['test_start_time'][-1], '%Y-%m-%d %H:%M:%S')
    #     end = datetime.strptime(test_case[test_id]['test_end_time'][-1],  '%Y-%m-%d %H:%M:%S')
    #     during = end - start
    #     self.update_test_content_list(job_id, test_id, 'test_during_time', str(during))

    # def get_job_information(self, job_id):
    #     job = self._database.find_one(ObjectId(job_id))
    #     return job

    def getJobstatusByJobID(self, job_id):
        return self._database.find_one({'_id':ObjectId(job_id)},{'_id':0,'status':1})

    def setJobResultByJobID(self, job_id):
        test_case_count = 0
        pass_count = 0
        fail_count = 0
        status = 'Finished'

        test_case_list = self._database.find({"_id":ObjectId(job_id)},{"testcase_list":1,"_id":0})[0]['testcase_list']

        for test_case in test_case_list:
            # total_times = float()
            # times = 0
            # FMT = '%H:%M:%S'
            # if isinstance(test_case['test_during_time'],list):
            #     time_list = test_case['test_during_time']
            #     for during_time in time_list:
            #         a = time.strptime(during_time,FMT)
            #         b = timedelta(hours=a.tm_hour, minutes=a.tm_min, seconds=a.tm_sec).total_seconds()
            #         total_times += b
            #         times += 1
            #     print(timedelta(seconds=(total_times / times)))
            if isinstance(test_case['test_result'],list):
                ## For SONiC Ansible result
                if len(test_case['test_result']) == 5 and 'OK' in test_case['test_result'][0]:
                    test_result = test_case['test_result'][4]
                    test_case_count += 1
                    if test_result == 'Success' or test_result == 'Pass':
                        pass_count += 1
                    elif 'Warning' in test_result or 'Failed' in test_result:
                        fail_count += 1
                elif len(test_case['test_result']) > 0:
                    for result in test_case['test_result']:
                        test_case_count += 1
                        if result == 'Success' or result == 'Pass':
                            pass_count += 1
                        elif result == 'Failed':
                            fail_count += 1
                else:
                    test_case_count += 1
            elif test_case['test_result'] == 'Success' or test_case['test_result'] == 'Pass':
                test_case_count += 1
                pass_count += 1
            elif test_case['test_result'] == 'Failed':
                test_case_count += 1
                fail_count += 1
        if pass_count + fail_count != test_case_count :
            status = 'Running'
        if status == 'Finished':
            if pass_count < test_case_count :
                result = 'Failed'
            else:
                result = 'Pass'
            self._database.update({'_id':ObjectId(job_id)},{'$set':{'result':result,'status':status}})