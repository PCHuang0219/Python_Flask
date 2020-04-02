import csv

with open('../Config/Server_Config.csv',newline='') as Server_config:
    data = csv.DictReader(Server_config)
    for row in data :
        web_server_ip = row['web_server_ip']
        web_server_port = row['web_server_port']
        DATABASE_IP = row['db_ip']
        DATABASE_PORT = int(row['db_port'])

with open('../Config/SONiC_Config.csv',newline='') as SONiC_config:
    data = csv.DictReader(SONiC_config)
    for row in data :
        docker_id = row['docker_id']
        docker_name = row['docker_name']
        docker_username = row['docker_username']
        config_server_username = row['config_server_username']
        config_server_ip = row['config_server_ip']
        config_server_password =row['config_server_password']
        config_file_path = row['config_file_path']

with open('../Config/test_case.csv',newline='') as test_case_list:
    global TEST_CASES_DICT
    TEST_CASES_DICT = {}
    data = csv.DictReader(test_case_list)
    for row in data :
        '''
        Purpose: Store test case information to TEST_CASES_DICT
        Parameter:
            Headline     = The headline of test case.
            TC_Number    = The code of test case.
            Import_class = The class of test case.
            Diag_type    = For minipack diag test.
        Format:
            TEST_CASES_DICT[Headline] = [TC_Number, Import_class, Diag_type]
        '''
        TEST_CASES_DICT[row["Headline"]]=[row["Test Case Number"], row["Import Method"], row["DiagType"]]

with open('../Config/DUT_Config.csv',newline='') as DUT_config:
    '''
    Purpose: Store DUTs information to DUT_DICT
    Parameter:
        model    = Name of model.
        ssh_ip   = The Mgmt IP of DUT.
        ssh_port = The ssh port default is 22.
        username = Username for login DUT.
        password = Password for login DUT.
        prompt   = Prompt of DUT.
    Format:
        DUT_DICT[model] = {ssh_ip=ssh_ip, ssh_port=ssh_port, username=username, password=password, prompt=prompt}
    '''
    global DUT_DICT
    global model_list
    model_list = []
    DUT_DICT = {}
    data = csv.DictReader(DUT_config)
    for row in data :
        if row['Role'] == 'DUT':
            DUT_DICT[row['Model']] = dict(ssh_ip = row['SSH_IP'], ssh_port = row['SSH_Port'], username = row['SSH_Username'], password= row['SSH_Password'], prompt= row['Prompt'])
            model_list.append(row['Model'])

def getAllDUTInformation(settings):
    '''
    --------------------------------------------------------------------
    Function name : getAllDUTInformation
    
    Headline      : Read DUT information from Config/DUT_Config.csv
    
    Purpose       : According to DUT selected by User executing the TCs.
    
    History       : 
          04/28/2019 - Anber Huang,Created
          10/02/2019 - Anber Huang,Modified
    
    Copyright(c): Accton Corporation, 2019
    --------------------------------------------------------------------
    '''
    with open('../Config/DUT_Config.csv',newline='') as DUT_config:
        data = csv.DictReader(DUT_config)
        for row in data :
            if row['Role'] == 'DUT' or row['Role'] == 'PDU':
                hostname = "'" + row['Hostname'] + "'"
                model = row['Model']
                platform = "'" + row['Platform'] + "'"

                COM_port = "'" + row["COM_port"] + "'"
                Baud_rate = row["Baud_rate"]

                console_port = "'" + row['Console_port'] + "'"
                console_server_ip = "'" + row['Console_server_ip'] + "'"
                
                SSH_IP = "'" + row['SSH_IP'] + "'"
                SSH_Netmask = "'" + row['SSH_Netmask'] + "'"
                SSH_Password = "'" + row['SSH_Password'] + "'"
                SSH_Username = "'" + row['SSH_Username'] + "'"
                SSH_Port = "'" + row['SSH_Port'] + "'"
                SSH_KeyFIlePath = "'" + row ['SSH_KeyFIlePath'] + "'"
                
                prompt = "'" + row['Prompt'] + "'"
                comment = row['Comment']

                console_credentials = '(' + "'console'," + COM_port + ',' + Baud_rate + ',' + SSH_Username + ',' + SSH_Password + ',' + prompt + ")"
                telnet_credentials = '(' + "'telnet'," + console_server_ip + ',' + console_port + ',' + SSH_Username + ',' + SSH_Password + ',' + prompt + ")"
                ssh_credentials = '(' + "'ssh'," + SSH_IP + ',' + SSH_Port + ',' + SSH_Username + ',' + SSH_Password + ',' + prompt + "," + ")"

                data = {"Model":model,"Hostname":hostname,"comment":comment,"platform":platform, \
                    "console_credentials":console_credentials,"telnet_credentials":telnet_credentials,"ssh_credentials":ssh_credentials, \
                    "SSH_Netmask":SSH_Netmask}

                addDUTToSettingsFile(data,settings)

def initSettingFile():
    '''
    --------------------------------------------------------------------
    Function name : initSettingFile
    
    Headline      : Generate settings.py from settings.init ( initial content )
    
    Purpose       : For all script get DUT information from Config/settings.py
    
    History       : 
          10/02/2019 - Anber Huang,Created
    
    Copyright(c): Accton Corporation, 2019
    --------------------------------------------------------------------
    '''
    open('../lib/settings.py', 'w').close()
    settings = open('../lib/settings.py','a')
    initContent = open('../lib/settings.init','r')
    settings.write(initContent.read())
    return settings

def addDUTToSettingsFile(data,settings):
    '''
    --------------------------------------------------------------------
    Function name : addDUTToSettingsFile
    
    Headline      : Create DUT as a class to settings.py
    
    Purpose       : For all script get DUT information from Config/settings.py
    
    History       : 
          10/02/2019 - Anber Huang,Created
    
    Copyright(c): Accton Corporation, 2019
    --------------------------------------------------------------------
    '''
    className = 'class ' + data["Model"] + '():\n'
    settings.write(className)
    settings.write("  def __init__(self):\n")
    DUTParameter = "    self.model_name = '" + data["Model"] + "'\n" + \
                   '    self.platform = ' + data["platform"] + '\n' + \
                   '    self.console_credentials = ' + data["console_credentials"] + '\n' + \
                   '    self.telnet_credentials = ' + data["telnet_credentials"] + '\n' + \
                   '    self.ssh_credentials = ' + data["ssh_credentials"] + '\n' + \
                   '    self.ssh_netmask = ' + data["SSH_Netmask"] + '\n\r'
    settings.write(DUTParameter)


def main():
    settings = initSettingFile()
    getAllDUTInformation(settings)
    settings.close()

if __name__=="__main__":
    main()