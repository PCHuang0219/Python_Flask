from threading import Thread
from multiprocessing import Process, Pipe

class Ansible_Job_Manager():
    def __init__(self):
        self.status = 'Finished'
        self.wait_job_list = []
        self.execute_job_list = []
    
    def set_status(self):
        wait_job_count = len(self.wait_job_list)
        execute_job_count = len(self.execute_job_list)                                                                                                                                                                                                                                              
        if execute_job_count > 0 :
            self.status = 'Busy'
        elif wait_job_count >0 and execute_job_count == 0 :
            self.status = 'Executable'
        else :
            self.status = 'Finished'

    def get_status(self):
        self.set_status()
        return self.status

    def add_job(self,job):
        self.wait_job_list.append(job)
        self.set_status()

    def get_new_job(self):
        if self.execute_job_list == [] :
            job = self.wait_job_list.pop(0)
            self.execute_job_list.append(job)
            self.set_status()
            print("ansible get new job" + job.job_id)
            ansible_manager_conn = str(job)+"manager"
            ansible_job_conn = str(job)
            ansible_manager_conn,ansible_job_conn = Pipe()
            p = Process(target=self.execute_job,args=(job,ansible_job_conn))
            p.start()
            t = Thread(target=self.check_job_status,args=(job,ansible_manager_conn))
            t.start()
        
    def execute_job(self,job,ansible_job_conn):
        print("ansible job run")
        job.execute_test_case()
        ansible_job_conn.send('Job Finished')
        print("job end")
    
    def check_job_status(self,job,ansible_manager_conn):
        while(1):
            if ansible_manager_conn.recv() == 'Job Finished' :
                self.execute_job_list.pop(0)
                self.set_status()
                break


