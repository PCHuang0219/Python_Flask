import pexpect

class Minipack():
    def __init__(self):
        self.username = "root"
        self.password = "1111"
        self.ip_address = "10.100.43.132"
        self.cmd = cmd = "sshpass -p " + self.password + " ssh " + self.username + "@" + self.ip_address
    
    def run_test_case(self,ID,test_type,log_file):
        status=open(log_file,"a")
        self.server = pexpect.spawn(self.cmd)
        self.server.expect(["#"])
        if test_type != "Stress":
            ID += 10000
            cmd = "diag_main_stress.py -m " + ID
            self.server.sendline(cmd)
            status.write(self.before)
            self.server.sendline(ID)
            self.server.expect(["Please enter your choice (0 to quit): "],timeout=None)
            status.write(self.before)
        else:
            self.server.sendline("diag_main.py")
            self.server.expect(["Please enter your choice (0 to quit): "],timeout=180)
            status.write(self.before)
            self.server.sendline(ID)
            self.server.expect(["Please enter your choice (0 to quit): "],timeout=None)
            status.write(self.before)