# Backend_Server

There are all code work on Backend Server.

### 1. Folder: Execute. There are all function for back_end server to control all job.
 The main file is app.py . It's run the flask server to create lots of API to connect Web Server.

### 2. Folder: Config. There are all configuration to configuare the detail.
* They need to store the 'csv' format. It's very important.
* DUT_Config.csv : That'is all DUT's port number,hostname,console server IP address.
* Server_Config.csv : That's Web server and Back_end server IP adress & port number setting.
* SONiC_Config.csv : That's SONiC test environment configuration .

### 3. Folder: SONiC. There are all script for Ansible and Non_ansible testcase.
* If you create the Non_Ansible testcase,please store it in Testcase_Script under the folder named FUNCTION.

* The testcase log will be create when the teastcase finished.
* The folder's name is "report",it is stored in the upper level.
* Under the "report",the folders will be create when job executes and is named it's job_id.

### 4. Files: This is a introduction of important files.
* Dockerfile : This is build an environment of Back_end Server, include Ubuntu Python3 Python3-pip docker.io
* requirements.txt : This is all library of Python3 need environment.

### If you want to run the server,execute the command:
* $ cd Execute/
* $ python3 app.py

### Quickly Start :
* Execute "start.sh" will build a docker image that provide Backend Server Service: 
* $ sh start.sh