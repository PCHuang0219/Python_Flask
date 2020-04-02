import sys
sys.path.append("..")
from Execute.Job import *
from Database.Data_Base import *
from SONiC.Ansible_Job_Manager import *
from SONiC.Non_Ansible_Job_Manager import *

class Job_Manager():
    def __init__(self):
        self.database = Data_Base()
        self.non_ansible_job_manager = Non_Ansible_Job_Manager()
        self.ansible_job_manager = Ansible_Job_Manager()
        self.status = 'Finished'

    def add_job(self,job) :
        if job.topo == "T_SONiC_Ansible" :
            self.ansible_job_manager.add_job(job)
        else:
            self.non_ansible_job_manager.add_job(job)

    def set_status(self):
        ansible_status = self.ansible_job_manager.get_status()
        non_ansible_status = self.non_ansible_job_manager.get_status()
        if ansible_status == 'Busy' and non_ansible_status == 'Busy' :
            self.status = 'Busy'
        elif ansible_status == 'Finished' and non_ansible_status == 'Finished' :
            self.status = 'Finished'
        else :
            self.status = 'Executable'
    
    def get_new_job(self) :
        self.ansible_job_manager.set_status()
        self.non_ansible_job_manager.set_status()
        if self.ansible_job_manager.get_status() == 'Executable' :
            self.ansible_job_manager.get_new_job()
        elif self.non_ansible_job_manager.get_status() == 'Executable' :
            self.non_ansible_job_manager.get_new_job()

    def get_status_log(self,job_id) :
        return self.database.get_status_log(job_id)