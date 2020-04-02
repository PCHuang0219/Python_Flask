# import pexpect
import sys
import os

test_type = sys.argv[2]
execute_file = "/usr/local/accton/bin/anber_auto.py "
test_item_no = sys.argv[1]

# cmd = "sshpass -p 1111 ssh root@10.100.43.132"
# DUT = pexpect.spawn(cmd)
# DUT.expect(["#"])
# DUT.sendline("sudo rm anber_sys_log")
# cmd = "python " + execute_file + test_item_no + " " + test_type + " >>anber_sys_log"
# print(cmd)
# DUT.sendline(cmd)
# DUT.expect(["#"],timeout=600)
# print(DUT)
# print("diag end")
delete_cmd = "sudo rm anber_sys_log"
cmd = "sshpass -p 1111 ssh root@10.100.43.132 '" + delete_cmd + "'"

os.system(cmd)
remote_cmd = "python " + execute_file + test_item_no + " " + test_type + " >>anber_sys_log"
cmd = "sshpass -p 1111 ssh root@10.100.43.132 '" + remote_cmd + "'"
os.system(cmd)
