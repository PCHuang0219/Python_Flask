from multiprocessing import Process, Pipe
from threading import Thread

class Non_Ansible_Job_Manager():

    def __init__(self):
        self.wait_job_list = []
        self.wait_job_model_list = []
        self.create_job_list = []
        self.create_job_model_list = []
        self.execute_job_list = []
        self.execute_job_model_list = []
        self.status = 'Finished'

    def set_status(self):
        wait_job_count = len(self.wait_job_list)
        create_job_count = len(self.create_job_list)
        execute_job_count = len(self.execute_job_list)
        if wait_job_count > 0 and create_job_count == 0 :
            self.status = 'Executable'
        elif create_job_count > 0 :
            self.status = 'Executable'
        elif create_job_count == 0 and execute_job_count >0 :
            self.status = 'Busy'
        else :
            self.status = 'Finished'
    
    def get_status(self):
        return self.status

    def add_job(self,job) :
        self.wait_job_list.append(job)
        self.wait_job_model_list.append(job.model)
        self.set_status()
    
    def get_new_job(self) :
        new_job = [job_model for job_model in self.wait_job_model_list if job_model not in self.execute_job_model_list ]
        if new_job != [] :
            print (new_job)
            for job in new_job :
                num = self.wait_job_model_list.index(job)
                self.create_job_model_list.append(self.wait_job_model_list.pop(num))
                self.create_job_list.append(self.wait_job_list.pop(num)) 
            for job in self.create_job_list :
                job = self.create_job_list.pop(0)
                job_model = self.create_job_model_list.pop(0)
                self.execute_job_list.append(job)
                self.execute_job_model_list.append(job_model)
                self.set_status()
                self.execute_job(job)
                # non_ansible_manager_conn,non_ansible_job_conn = Pipe()
                # p = Process(target=self.execute_job,args=(job,non_ansible_job_conn))
                # p.start()
                # t = Thread(target=self.check_job_status,args=(job,non_ansible_manager_conn))
                # t.start()

    def execute_job(self,job) :
        print("non_ansible job run")
        job.set_start_status()
        job.execute_test_case()
        print("non_ansible job end")
        # non_ansible_job_conn.send('Job Finished')
    
    def check_job_status(self,job,non_ansible_manager_conn):
        while(1):
            if non_ansible_manager_conn.recv() == 'Job Finished' :
                execute_num = self.execute_job_list.index(job)
                self.execute_job_list.pop(execute_num)
                self.execute_job_model_list.pop(execute_num)
                self.set_status()
                break

