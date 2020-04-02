#!/usr/bin/python3
"""
Module Name: app.py
Purpose: Flask app module

Description:
    This module uses Python Flask module which is the simple web framework. To provide RESTful API to communicate with
    front-end of TMS.
History:
    Anber Huang 06/30/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

import sys
sys.path.append("..")
from Config.get_all_config import *
from Job_Management.job_manager import Job_Manager
from Database.database import Data_Base
from Execute.job import *
from flask import Flask, jsonify, abort, request
import time
import urllib3
import threading
import subprocess

data_base = Data_Base()
job_manager = Job_Manager()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
app = Flask(__name__)

def Run(): 
    #It is a while loop to check job_manager status and submit a job executed .
    while(1):
        job_manager.set_status()
        if job_manager.status == 'Finished':
            #print("no job")
            time.sleep(0.5)
        elif job_manager.status  == 'Executable' :
            print("run")
            job_manager.get_new_job()
            time.sleep(5)
        elif job_manager.status == 'busy' :
            print("wait")

t = threading.Thread(target=Run)
t.setDaemon(True)
t.start()

@app.route('/getDUTList', methods=['GET'])
def get_DUT_list():
    return jsonify({'DUTList':model_list})

## Anber: Bug need to fix
# @app.route('/getTestcasesList', methods=['GET'])
# def get_testcases_list():
#     testcases_list = data_base.get_testcases_list
#     print(testcases_list)
#     return jsonify({'testcases_list':testcases_list})

'''
RESTful API Name: "http://SERVER_IP:8000/jobLog"
Description: 
    Return current job status log from status file under named own job_id folder.
Parameter:
    - job_id: The ID of this job.
Note:
    SERVER_IP can use any IPs on this device.
    Default port using port 8000, please referent the bottom of this file.
History:
    Anber Huang 02/13/2020,created.

Copyright(c) Accton Technology Corporation, 2019.
'''
@app.route('/jobLog', methods=['GET'])
def job_status_log():
    data = request.form
    job_id = data['job_id']
    platform = data ['platform']
    log = job_manager.get_status_log(job_id,platform)
    return jsonify({'log':log})

'''
RESTful API Name: "http://SERVER_IP:8000/submitJob"
Description: 
    Submit job from front-end user select and click submit button.
Parameter:
    - job_id: The ID of this job.
Note:
    SERVER_IP can use any IPs on this device.
    Default port using port 8000, please referent the bottom of this file.
History:
    Anber Huang 02/13/2020,created.

Copyright(c) Accton Technology Corporation, 2019.
'''
@app.route('/submitJob', methods=['POST'])
def create_job():
    data = request.form
    job_id = data['job_id']

    # Get job data from database by job_id
    job = data_base.get_job_information(job_id)
    job_name = job["job_name"]
    job_topo = job["testcase_topology"]
    job_model = job["model"]
    job_platform = job["platform"]
    image_version = job["image_version"]

    # Write job information to "class Job(job_id)"
    JOB = Job(job_id)
    JOB.set_information(job_topo, job_model, job_platform, job_name, image_version)
    job_test_list = job["testcase_list"]
    # Get all testcases detail data
    test_list = []
    stage_list = []
    try:
        stage_num = job_test_list[0]["test_stage_id"]
    except:
        stage_num = '0'
    for testcases in job_test_list :
        try:
            stage_id = testcases["test_stage_id"]
        except:
            stage_id = '0'
        testcases["job_id"] = job_id
        if stage_id == stage_num:
            test_list.append(testcases)
        else:
            stage_num = stage_id
            stage_list.append(test_list)
            test_list = []
            test_list.append(testcases)
        
        if testcases == job_test_list[-1]:
            stage_list.append(test_list)

    JOB.add_test(stage_list)
    job_manager.add_job(JOB)
    job_manager.set_status()
    return jsonify({'success': 'Success'})

# @app.route('/currentTestcaseName', methods=['GET'])
# def current_testcase():
#     data = request.form
#     job_id = data['job_id']
#     job = job_manager.get_job_by_jobid(job_id)
#     return jsonify({'name':"job"})

# @app.route('/jobConfigure', methods=['GET'])
# def config():
#     data = request.form
#     print(data)
#     job_id = data['job_id']
#     job = Job(job_id)
#     return jsonify({'configure':{'topo':job.topo,'model':job.model,'platform':job.platform}})

# @app.route('/jobStatus', methods=['GET'])
# def job_status():
#     data = request.form
#     print(data)    
#     job_id = data['job_id']
#     job = Job(job_id)   
#     print("status :"+job.get_job_status())
#     return jsonify({'status':job.get_job_status()})

# @app.route('/jobProgress', methods=['GET'])
# def progress():
#     data = request.form
#     print(data)    
#     job_id = data['job_id']
#     job = Job(job_id)
#     print("progress :"+job.get_percent_finish())
#     return jsonify({'progress':job.get_percent_finish()})

# @app.route('/jobExecuteTime', methods=['GET'])
# def job_execute_time():
#     data = request.form
#     print(data)    
#     job_id = data['job_id']
#     job = Job(job_id)
#     print("execute_Time:"+job.get_running_time())
#     return jsonify({'time':job.get_running_time()})

# @app.route('/testTableInJob', methods=['GET'])
# def testTableInJob():
#     data = request.form
#     print(data)    
#     job_id = data['job_id']
#     job = Job(job_id)
#     return jsonify({'testTable':job.get_job_detail()})

if __name__ == '__main__':
    # Generate lib/settings.py Class DUT
    subprocess.call(['python3','../Config/get_all_config.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    app.run(host='0.0.0.0', debug=True, port=8000 ,use_reloader=False)