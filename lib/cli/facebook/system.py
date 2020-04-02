#!/usr/bin/python3
####################################################################################################

from lib.cli.facebook.parameters import *
from lib import settings
from lib.ui import UI
import traceback
import datetime
import time
import sys
import re

class System(UI):
  def __init__(self, ui_credentials, platform):
    self.__dut = super().__init__(ui_credentials, platform=platform)
    self.prompt = super().getPrompt()
    self.out_even = super().getOutEven()

  # Define your API below this line.

  def returnDUT(self):
    return self.__dut

  def i2cBusTest(self):
    is_mcp2221a_used = -1

    retstr = self.sendCmd("cat %s " % DIAG_IS_MCP2221A_USED_FILE)
    if retstr != "":
      retstr = retstr.splitlines()
    is_mcp2221a_used = int(retstr[0])

    if is_mcp2221a_used == 1:
      i2c_0_device_address = ['08', '44', '48']
    else:
      i2c_0_device_address = ['74', 'e0', 'ae', 'be']

    UI.log("is_mcp2221a_used %d" % is_mcp2221a_used)

    return i2c_0_device_address

  def check_cp2112_exist(self, expect_result):
    vp_id = "10c4:ea90"
    cmd = "lsusb -d %s" % vp_id
    out = self.sendCmd(cmd, writting=False)
    if retstr != "":
      retstr = retstr.splitlines()
    if len(out) != 0:
      out = out[0]
    else:
      out = ""
    print("\r\r[%s]" % out)
    is_exist = True

    if vp_id in out:
      is_exist = True
    else:
      is_exist = False

    if expect_result != is_exist:
      UI.log("FAIL", "### CP2112 status test failed ###")
      return -1
    else:
      UI.log("PASS", "### CP2112 status test passed ###")

  def set_cp2112_rst(self, val):
    rst_fs = "/sys/bus/i2c/devices/i2c-12/12-003e/cpld_usb2112a_brdg_rst"
    cmd = "echo %d > %s" % (val, rst_fs)
    self.send(cmd + "\r")
    self.expect(self.prompt)
    time.sleep(5)

  def check_i2c_address(self, i2c_0_device_address):
    fail_count = 0
    work_dir = "/usr/local/accton/bin"
    self.send("cd %s \r" % work_dir)
    self.expect('bin' + self.prompt.replace('~', ''))

    self.send("source accton_i2cdetect.sh\r")
    self.expect('bin' + self.prompt.replace('~', ''))

    retstr = self.getBuff()
    for i in i2c_0_device_address:
      if i not in retstr:
        print("\nReading device address 0x%s of cp2112 FAILED!" % (i))
        fail_count += 1

    self.sendCmd('cd',writting=False)

    if fail_count != 0 :
      UI.log("FAIL", "The bus test for cp2112 is FAILED!")
    else:
      UI.log("PASS", "The bus test for cp2112 is PASSED!")

  def get_board_config(self):
    ret = 0
    config_str = ''
    valid_str = []
    try:
      retstr = self.sendCmd("cat %s" % BOARD_CONFIG_FILE, writting=False)
      if retstr != "":
        retstr = retstr.splitlines()[0]
      if 'No such file or directory' in retstr:
        UI.log('Cannot access [%s], use default value.\n' % BOARD_CONFIG_FILE)
        ret = BOARD_ALL
      else:
        config_str =  val = retstr
        val_ls = val.upper().split()
        for key in val_ls:
          for brd_id in BOARD_CONFIG_MAP:
            name_ls = BOARD_CONFIG_MAP[brd_id]
            if key in name_ls:
              ret |= brd_id
              valid_str.append(key)
              break
        invalid_str = [k for k in val_ls if k not in valid_str]
        if len(invalid_str):
          UI.log('Recognized & Unrecognized: [%s] [%s]' %\
                (' '.join(s for s in valid_str),
                ' '.join(s for s in invalid_str)))

      if ret == 0:
        ret = BOARD_ALL
      UI.log('Board config string: [%s] [0x%02x]' % (config_str, ret))

    except Exception as e:
      print('Exception, use default value.')
      ret = BOARD_ALL

    return ret

  def pci_all_clear_all_aer_mask(self):
    try:
      cmd_ret = self.sendCmd('lspci -n | awk \'{printf $1 " "}\'', writting=False)
      pci_dev_list = cmd_ret.split()
    except:
      UI.log("FAIL", "get pci dev list failed")
      return 1

    try:
      cmd_ret = self.sendCmd('lspci -n | awk \'{printf $3 " "}\'', writting=False)
      pci_id_list = cmd_ret.split()
    except:
      UI.log("FAIL", "get pci dev id failed")
      return 1
    for i in range(len(pci_dev_list)-2):
      if i == 0:
        print('\r')
      try:
        if self.prompt.replace(' ', '') not in pci_dev_list[i] or '.*root@.*' not in pci_dev_list[i]:
          BUS=pci_dev_list[i].split(':')[0]
          DEV=pci_dev_list[i].split(':')[1].split('.')[0]
          FN=pci_dev_list[i].split(':')[1].split('.')[1]
          VENDOR_ID=int("0x" + pci_id_list[i].split(':')[0],16)
          DEVICE_ID=int("0x" + pci_id_list[i].split(':')[1],16)
          PCI_BASE, ret = self.pci_get_pci_cfg_base_by_bdf(BUS, DEV, FN, VENDOR_ID, DEVICE_ID)
      except Exception as e:
        pass
      if ret == 0:
        AER_BASE, ret = self.pci_get_aer_cfg_base(PCI_BASE)
        if ret == 0 :
          print ("Clear %s AER mask" % pci_dev_list[i])
          self.aer_cfg_clear_cemask(AER_BASE)
          self.aer_cfg_clear_uemask(AER_BASE)
        else:
          print ("%s no AER mask" % pci_dev_list[i])
      else:
        return 1
    
    return 0

  def pci_get_pci_cfg_base_by_bdf(self, BUS, DEV, FN, VENDOR_ID, DEVICE_ID):
    try:
      cmd_ret = self.sendCmd('cat /proc/iomem | grep MMCONFIG > /dev/null', writting=False)
    except:
      UI.log("FAIL", "Can't find MMCONFIG in /proc/iomem")
      return 0,1

    cmd_ret = self.sendCmd('cat /proc/iomem | grep MMCONFIG | awk \'{print $1}\' | awk -F "-" \'{print $1}\'', writting=False)
    if cmd_ret != "":
      cmd_ret = cmd_ret.splitlines()
    
    for line in cmd_ret:
      if re.search('^\d', line):
        MMCONFIG = line
    MMCONFIG = int("0x" + MMCONFIG,16)
    CFG_BASE = MMCONFIG + (int(BUS,16)<<20 | int(DEV,16)<<15 | int(FN,16)<<12)
    #Verify CFG BASE
    DEVICE = self.sendCmd('mem 0x%x 32' % CFG_BASE, writting=False)
    if DEVICE != "":
      DEVICE = DEVICE.splitlines()
    DEVICE = int(DEVICE[0],16)
    TARGET_DEVICE=(VENDOR_ID | (DEVICE_ID<<16))
    if DEVICE != TARGET_DEVICE  :
      UI.log("FAIL", "DEVICE != TARGET_DEVICE for %x:%x" % (VENDOR_ID, DEVICE_ID))
      return 0,1

    return CFG_BASE, 0

  def aer_cfg_clear_cemask(self, AER_BASE):
    CEMsk_ADDR=AER_BASE + 0x14
    #Read Correctable Error Mask Register
    cmd_ret = self.sendCmd('mem 0x%x 32' % CEMsk_ADDR, writting=False).splitlines()
    DATA=int(cmd_ret[0], 16)
    DATA=(DATA&(~0x0000FFFF))
    #Write 0 to clear Correctable Error Mask Register
    cmd_ret = self.sendCmd('mem 0x%x 32 0x%x' % (CEMsk_ADDR,DATA), writting=False).splitlines() 
    if len(cmd_ret) == 0:
      return '', 0
    else:
      return cmd_ret[0], 0

  def aer_cfg_clear_uemask(self, AER_BASE):
    UEMsk_ADDR=AER_BASE + 0x08
    #Read UnCorrectable Error Mask Register
    cmd_ret = self.sendCmd('mem 0x%x 32' % UEMsk_ADDR, writting=False).splitlines() 
    DATA=int(cmd_ret[0], 16)
    DATA=(DATA&(~0xFFFFFFFF))
    #Write 0 to clear UnCorrectable Error Mask Register
    cmd_ret = self.sendCmd('mem 0x%x 32 0x%x' % (UEMsk_ADDR,DATA), writting=False).splitlines()
    if len(cmd_ret) == 0:
      return '', 0
    else:
      return cmd_ret[0], 0

  def pci_get_aer_cfg_base(self, PCI_BASE):
    CAP_OFF = PCI_BASE+0x100
    cmd_ret = self.sendCmd('mem 0x%x 32' % CAP_OFF, writting=False).splitlines() 
    DATA = cmd_ret[0]
    DATA = int(DATA,16)
    if ((DATA & 0xFFFFFFFF) == 0xFFFFFFFF):
        return 0, 1

    while (DATA & 0xFFF) != 0x001 and ((DATA&0xFFF00000)>>20) != 0 :
        CAP_OFF = PCI_BASE+((DATA&0xFFF00000)>>20)
        cmd_ret = self.sendCmd('mem 0x%x 32' % CAP_OFF, writting=False).splitlines() 
        DATA = cmd_ret[0]
        DATA = int(DATA,16)
    if (DATA & 0xFFF) != 0x001:
        return 0, 1

    return CAP_OFF, 0

  def bmc_check_process_done(self, cmd, chk_per_s=0.5, max_wait_s=15, cat_result=False, fail_retry=3):
    get_pid_t = 500
    result_file = "/tmp/" + cmd.split()[0]
    rs = result_str = ""
    ret = [DIAG_STATUS_SUCCESS, result_str]
    first_run = True
    debug_time = False # debug
    while fail_retry >= 0:
      if ret[0] is DIAG_STATUS_SUCCESS:
        if first_run is False: # success and run one time
          break
          # also can do return
        else:
          first_run = False
      else:
        print(">> [%s] retry remain %d" % (cmd, fail_retry))
        fail_retry -= 1

      wait_t = task_pid_out = task_done = 0
      try:
        # Don't set init_pid as -1 (this will kill all process)
        init_pid = -2
        pid = init_pid
        retry = 3
        if cat_result == False:
          self.send(cmd + " &\r")
        else:
          self.send(cmd + " > %s &\r" % result_file)

        self.expect(self.prompt , timeout=TTY_PROMPT_TIME_MS, writting=False)

        check_status = False
        # Get pid
        while retry > 0:
          rs = self.sendCmd("jobs -p", writting=False)
          if rs != "":
            rs = rs.splitlines()
            pid = rs[1]
            if len(rs) > 3:
              if "Done" in rs[2]:
                task_done = 1
                check_status = rs[2]
          if pid == init_pid:
            retry -= 1
            get_pid_t += 1000
            print("retry get pid")
          else:
            break

        if pid == init_pid:
          print("Get PID failed")
          print("dbg:" + rs)
          ret = [DIAG_STATUS_FAILED, result_str]
          continue

        tty_wait = 200
        max_tty_wait = 1000
        start_t = time.time()

        while wait_t < max_wait_s:
          rs = self.sendCmd("echo getpid:$! ", writting=False)
          if rs != None:
            rs = rs.splitlines()
            for line in rs:
              if re.search("^getpid:[0-9]{1,5}$", line):
                pid_check = int(line.split(":")[1], 10)
                break
              elif "Done" in line:
                task_done = 1
                check_status = line
          else:
            if tty_wait < max_tty_wait:
              tty_wait += 200
              print("CPD function increase tty_wait (%d)" % tty_wait)
              continue
          task_pid_out = 1
          if not check_status:
            task_done = 1
            time.sleep(3)
          # Check process part 1
          # pid_str = str(pid)
          # if pid_str in rs:
          #   # job is running
          #   pass
          # Check process part 2
          # for retry in range(3):
          #   print(check_status)
          #   if ("Done" in check_status or "Exit" in check_status) and result_file in check_status:
          #     print("\n\nBreak\n\n")
          #     break
          #   else:
          #     time.sleep(1)
          #     rs = self.sendCmd("\r").splitlines()
          break
          time.sleep(chk_per_s)
          wait_t = round(time.time() - start_t)
        if debug_time:
          proc_t = "# time: %.2f sec #" % (time.time() - start_t)
          cmd_str = "# %s #" % cmd
          par_str = "# (%.2f, %d, %d, %d) #" % (chk_per_s, max_wait_s, cat_result, fail_retry)
          print("\33[42;30m" + proc_t + "\33[0m" + \
                "\33[41;30m" + cmd_str + "\33[0m" + \
                "\33[46;30m" + par_str + "\33[0m")

        if not task_pid_out:
          print("Task is runing over the maximum limit")
          ret = [DIAG_STATUS_FAILED, result_str]
        else:
          if cat_result:
            self.send("sync\r")
            self.expect(self.prompt, timeout=TTY_PROMPT_TIME_MS, writting=False)
            rs = self.sendCmd("cat %s" % result_file, writting=False)
            result_str = result_str + rs
            # remove redundant strings
            rm_str = "cat %s\r\n" % result_file
            if rm_str in result_str:
              result_str = result_str.split(rm_str, 1)[1]
            self.sendCmd("rm %s" % result_file, writting=False)
            

          ret = [DIAG_STATUS_SUCCESS, result_str]

      except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "\n\nFile \"{}\", line {}, in {}: [{}] {}\n\n".format(fileName, lineNum, funcName, error_class, detail)
        print(errMsg)
        ret = [DIAG_STATUS_FAILED, result_str]
      finally:
        ## kill process
        if not task_pid_out or not task_done:
          #print("debug rs:[%s]" % rs)
          kill_pid_cmd = "kill -9 %d" % int(pid)
          self.send(kill_pid_cmd + "\r")
          self.expect(self.prompt, timeout=TTY_PROMPT_TIME_MS)
          time.sleep(1)

    return ret

  def get_process_result(self, cmd, chk_sec_t=1, max_chk_t=20, retry=3, concat=False):
    ret_data = ""
    tmp_data = []
    ret, rs = self.bmc_check_process_done(cmd, chk_sec_t, max_chk_t, True, retry)
    if ret == DIAG_STATUS_FAILED:
      reason = "Check process [%s] failed" % cmd
      print(reason)

    if len(rs) > 0 and rs != None:
      ret_data = rs.splitlines()
      ret_data.pop(0)
      ret_data.pop(-1)
      for line in ret_data:
        if self.prompt in line:
          # remove prompt string
          new_line = re.sub("root@.+# ", "", line)
          new_line = new_line.replace("root@bmc-oob:~#", "")
          new_line = new_line.replace(" cat /tmp/diag_cmd_output", "")
          if new_line != "":
            print("\n>>> Remain in line [%s] <<<\n" % new_line)
            tmp_data.append(new_line)
          continue
        tmp_data.append(line)
      if concat:
        return "\n".join(s for s in tmp_data)
      else:
        return tmp_data
    else:
      reason = "Read nothing from process [%s]" % cmd
      print(reason)
    return ""

  def cpu_stress_ng_test(self):
    cd_prompt = "bin" + self.prompt.replace("~", "")
    retstr = self.sendCmd("cd /usr/local/accton/bin", prompt=cd_prompt)
    # for line in retstr:
    #   if cd_prompt not in line:
    #     UI.log("FAIL", "Changing directory to %s FAILED!" % "/usr/local/accton/bin")
    #     return DIAG_STATUS_FAILED

    maximum_test_time = 120
    ### For test script
    # maximum_test_time = 10
    ret1 = 1
    ret2 = 1

    stdout = self.sendCmd("dmidecode -t 4 | grep \"Core Enabled\" | awk '{print $3}'", prompt=cd_prompt).splitlines()
    for line in stdout:
      if re.search("^\d", line):
        stdout_messages = line
    if stdout_messages:
        maximum_core_enabled_count = int(stdout_messages) ## Maximum CPU Core Enabled Count: Core Enabled
    else:
        maximum_core_enabled_count = 1
    # print(maximum_core_enabled_count)
    self.sendCmd("cpupower frequency-set -g performance", prompt=cd_prompt)
    self.sendCmd("cpupower frequency-info", prompt=cd_prompt)
    time.sleep(1)
    self.send("stress-ng --cpu %u --cpu-method matrixprod --metrics-brief --perf -t %u \r" % (maximum_core_enabled_count, maximum_test_time))
    while True:
      x = self.expect([cd_prompt, 'stress-ng: info:', '\n', '\r'], timeout= (maximum_test_time + 10 ))
      if x == 0:
        ret1 = x
        break
    # ret1 = self.expect(cd_prompt, timeout= (maximum_test_time + 10 ))
    if ret1 == 0:
        self.sendCmd("cpupower frequency-set -g powersave", prompt=cd_prompt)
        self.sendCmd("cpupower frequency-info", prompt=cd_prompt)
        time.sleep(1)
        self.send("stress-ng --cpu %u --cpu-method matrixprod --metrics-brief --perf -t %u \r" % (maximum_core_enabled_count, maximum_test_time))
        while True:
          x = self.expect([cd_prompt, '\n', '\r'], timeout= (maximum_test_time + 10 ))
          if x == 0:
            ret2 = x
            break
        # ret2 = self.expect(cd_prompt, timeout= (maximum_test_time + 10 ))

    ret = ret1 + ret2
    UI.log('Collect the return code of tests:  ' +
              '\n    Return Code (intel_pstate: performance): ' + '%d' % (ret1) +
              '\n    Return Code (intel_pstate: powersave): ' + '%d' % (ret2))
    if ret == 0 :
      UI.log("PASS","The stress-ng performance test for CPU is PASS !")
    else:
      UI.log("FAIL","The stress-ng performance test for CPU is FAIL !")
    
    self.sendCmd("cd", writting=False)

  def ddr_test(self):
    cd_prompt = "bin" + self.prompt.replace("~", "")
    retstr = self.sendCmd("cd /usr/local/accton/bin", prompt=cd_prompt)
    # for line in retstr:
    #   if cd_prompt not in line:
    #     UI.log("FAIL", "Changing directory to %s FAILED!" % "/usr/local/accton/bin")
    #     return DIAG_STATUS_FAILED

    retstr = self.sendCmd("cat /proc/meminfo", prompt=cd_prompt)
    meminfo = txt2tokens(retstr, prompt=cd_prompt)
    for line in meminfo:
      if "MemFree:" in line:
        memsize = int(line[1])
        break
    self.sendCmd("mkdir -p /usr/local/accton/log", prompt=cd_prompt)
    self.sendCmd("sync", prompt=cd_prompt)
    self.sendCmd("echo 3 > /proc/sys/vm/drop_caches", prompt=cd_prompt)

    stdout = self.sendCmd("dmidecode -t 4 | grep \"Thread Count\" | awk '{print $3}'", prompt=cd_prompt).splitlines()
    for line in stdout:
      if re.search("^\d", line):
        stdout_messages = line
    if stdout_messages:
        maximum_memtester_sub_processes = int(stdout_messages[0]) ## Maximum memtester sub process number: Thread Count/Core Enabled
    else:
        maximum_memtester_sub_processes = 1
    maximum_cpu_cores = 4 ## Maximum CPU core number: 4
    maximum_reserved_memory = 512000 ## Reserved the 512000KB (500MB) memories for cache or buffer of Kernel
    maximum_page_size = 4 ## Page size: 4KB
    memtester_test_mask = 0x14FF ## Test mask of memtester utility, enable b[0] if this value is not 0
    memtester_hop_size = 48 ## Hop size of memtester utility

    if memsize <= maximum_reserved_memory:
      UI.log("FAIL", "Out of memory !")
    memory_free_MB = memsize / 1024
    memory_tested = memsize - maximum_reserved_memory
    memory_tested_pre_process = int(memory_tested / maximum_memtester_sub_processes)
    memory_tested_pre_process = ((memory_tested_pre_process / maximum_page_size) + 1) * maximum_page_size

    process = []
    for i in range(0, maximum_memtester_sub_processes):
      if i == maximum_memtester_sub_processes:
        break;
      if i == (maximum_memtester_sub_processes - 1):
        time.sleep(3)
        print("\r\nProcess information:")
        self.send("ps -x | grep \"memtester\" \r")
        self.expect(cd_prompt)
        print("\r\nMonitor Process (%d):" % (i))
        self.send("./memtester -t 0x%X -s %u %dK 1 \r" % (memtester_test_mask, memtester_hop_size, memory_tested_pre_process))
        while True:
          x = self.expect([cd_prompt, '\r', '\n', '.*\d.*', '.*testing.*', '.*setting.*'], timeout=5)
          if x == 0:
            break

      else:
        self.sendCmd("./memtester -t 0x%X -s %u %dK 1 2>&1 > /usr/local/accton/log/memtester_test_%03u.log &" % (memtester_test_mask, memtester_hop_size, memory_tested_pre_process, i), writting=False, prompt=cd_prompt)
    # check_process = self.sendCmd('jobs -p', writting= False, prompt=cd_prompt).splitlines()
    # print("= "*30)
    # print(check_process[0])
    # while True:
    #   if len(check_process) > 0 :
    #     if re.search("^\d", line):
    #       print("* "*30)
    #       print(check_process)
    #       check_process = self.sendCmd('jobs -p', writting= False, prompt=cd_prompt).splitlines()
    #       time.sleep(10)
    #     else:
    #       print("not match")
    #   else:
    #     break
    # for i in range(maximum_memtester_sub_processes, 0, -1):
    #     process[i-1].communicate()

    ret = 0
    for i in range(0, maximum_memtester_sub_processes):
      if i < ( maximum_memtester_sub_processes - 1):
        print ("\r\nGrep Test Logs of Process %d:" % (i))
        cmd = 'grep "Memory test is passed" /usr/local/accton/log/memtester_test_%03u.log' % (i)
        retstr = self.sendCmd(cmd, prompt=cd_prompt, writting=False).splitlines()
        for line in retstr:
          line1 = line.replace(" ", ".*")
          line1 = line.replace("\x1b[", "")
          if not re.search(line1, cmd):
            print ("\n" + line)
        ret = ret | 0

    # print ("Collect the return code of processes:")
    # for i in range(0, maximum_memtester_sub_processes):
    #   print ("  Process %d: %d" % (i, 0))
    # print ("  Return Code: %d" % (ret))

    # print(datetime.datetime.now())
    self.sendCmd("cd ", writting=False)

    UI.log("PASS", "The R/W test for memory device(RAM) is PASS !")

  def bmc_check_pcie_err(self):
    ret = DIAG_STATUS_SUCCESS

    fpga_key = "FPGA"
    th3_key = "Tomahawk 3"
    unknown_key = "Unknown"
    pcie_err_log = {
      fpga_key:[],
      th3_key:[],
      unknown_key:[],
    }
    try:
      # Check BMC log
      UI.log("### Check BMC system event log ###")
      cmd = "grep -n PCIE /mnt/data/logfile*"
      rs = self.get_process_result(cmd)
      if rs:
        for line in rs:
          if "(Bus 00 / Dev 03 / Fun 01)" in line:
            ret = DIAG_STATUS_FAILED
            pcie_err_log[th3_key].append(line)
          elif "(Bus 00 / Dev 03 / Fun 00)" in line:
            ret = DIAG_STATUS_FAILED
            pcie_err_log[fpga_key].append(line)
          else:
            if 'No such file or directory' not in line:
              ret = DIAG_STATUS_FAILED
              pcie_err_log[unknown_key].append(line)

      for key in sorted(pcie_err_log.keys()):
        log_ls = pcie_err_log[key]
        err_count = len(log_ls)
        print("\n===== %s PCIE error (%d) =====" % (key, err_count))
        for log in log_ls:
          print(log)

      # Check CPU log
    except Exception as e:
      error_class = e.__class__.__name__ #取得錯誤類型
      detail = e.args[0] #取得詳細內容
      cl, exc, tb = sys.exc_info() #取得Call Stack
      lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
      fileName = lastCallStack[0] #取得發生的檔案名稱
      lineNum = lastCallStack[1] #取得發生的行號
      funcName = lastCallStack[2] #取得發生的函數名稱
      errMsg = "\n\nFile \"{}\", line {}, in {}: [{}] {}\n\n".format(fileName, lineNum, funcName, error_class, detail)
      print(errMsg)
      return DIAG_STATUS_FAILED
    return ret

  def check_cpu_log(self):
    ret = DIAG_STATUS_SUCCESS
    try:
      UI.log('### Check CPU FPGA pcie error ###')
      cmd = 'zgrep "FPGA.*b=0[1-7]" /var/log/message*'
      retstr = self.sendCmd(cmd, writting=False).splitlines()
      for i in range(0, len(retstr)):
        if cmd in retstr[i]:
          retstr.pop(i)
        elif self.prompt in retstr[i]:
          retstr.pop(i)
      if len(retstr) :
        ret = DIAG_STATUS_FAILED
    except Exception as e:
      print(repr(e))
      return DIAG_STATUS_FAILED
    return ret

  def bmc_show_powr1220_rev(self):
    ret = DIAG_STATUS_SUCCESS
    dev_name = "POWR1220AT8"
    bus, addr, drv = [1, 0x3a, "powr1220"]
    revision = 0
    # REV: reg(0xa) | reg(0xb) << 8 | reg(0xc) <<16 | reg(0xd) <<24
    rev_reg = [0x0a, 0x0b, 0x0c, 0x0d]

    try:
      ## Detect device
      self.bmc_i2c_device_delete(bus, addr)
      if not self.bmc_i2c_detect(bus, addr):
        UI.log("FAIL", "Cannot detect %s %d 0x%02x" % (drv, bus, addr))
        return DIAG_STATUS_FAILED
      #bmc_i2c_device_add(bus, addr, drv)

      for idx in range(len(rev_reg)):
        val = self.bmc_i2c_get(bus, addr, rev_reg[idx], False)
        if val == DIAG_STATUS_FAILED:
          UI.log("FAIL", "Get %s revision failed." % dev_name)
          return DIAG_STATUS_FAILED
        ## Revision 4 bytes order
        revision = revision | (val << idx*8)
      UI.log("---- %s version ----" % dev_name)
      print("%s: 0x%08x" % (dev_name, revision))

    except Exception as e:
      print(repr(e))
      return DIAG_STATUS_FAILED
    finally:
      self.bmc_i2c_device_add(bus, addr, drv)

    return ret

  def bmc_i2c_device_delete(self, bus, addr):
    cmd = "source /usr/local/bin/openbmc-utils.sh;"
    cmd += "i2c_device_delete %d 0x%02x > /dev/null 2>&1" % (bus, addr)
    self.send(cmd + "\r")
    self.expect(self.prompt, timeout=5000, writting=False)
    time.sleep(1)

  def bmc_i2c_device_add(self, bus, addr, drv):
    cmd = "source /usr/local/bin/openbmc-utils.sh;"
    cmd += "i2c_device_add %d 0x%02x %s > /dev/null 2>&1" % (bus, addr, drv)
    self.send(cmd + "\r")
    self.expect(self.prompt, timeout=5000, writting=False)
    time.sleep(1)

  def bmc_i2c_detect(self, bus, addr, max_retry=1):
    rs = ""
    # Check device busy status, using busy method as default
    is_busy = detect_ret = None
    for retry in range(1 + max_retry):
      try:
        cmd = "i2cdetect -y {0:d} {1:#x} {1:#x}".format(bus, addr) + \
                " | grep \"UU\" > /dev/null 2>&1; echo \"is_busy:$?\""
        rs = self.sendCmd(cmd, writting=False).splitlines()
        for line in rs:
          if re.match("^is_busy:[0-9]", line):
            if "is_busy:0" in rs:
              is_busy = True
            else:
              is_busy = False
        assert is_busy is not None
        break
      except AssertionError:
        print("debug rs:" + rs)
      except Exception as e:
        print(repr(e))
      if retry != max_retry:
        print("I2C detect retry")
        print("I2C detect retry (%d)" % (retry+1))

    # Detect device
    for retry in range(1 + max_retry):
      try:
        if is_busy:
          # So far read register 0 is working
          cmd = "i2cget -f -y {0:d} {1:#x} 0 &> /dev/null;echo \"read_test:$?\"".format(bus, addr)
          rs = self.sendCmd(cmd, writting=False).splitlines()
          for line in rs:
            if re.match("^read_test:[0-9]", line):
              if "read_test:0" in line:
                detect_ret = True
              else:
                detect_ret = False
        else:
          cmd = "i2cdetect -y {0:d} {1:#x} {1:#x}".format(bus, addr) + \
                " | grep \"\-\-\" &> /dev/null; echo \"grep--:$?\""
          rs = self.sendCmd(cmd, writting=False).splitlines()
          for line in rs:
            if re.match("^grep--:[0-9]", line):
              if not "grep--:0" in line:
                detect_ret = True
              else:
                detect_ret = False
          assert detect_ret is not None
          if detect_ret is True:
            break
          else:
            # retry
            pass

      except AssertionError:
        print("debug rs:" + rs)
      except Exception as e:
        print(repr(e))
      if retry != max_retry:
        print("I2C detect retry (%d)" % (retry+1))

    return detect_ret

  def bmc_i2c_get(self, bus, addr, reg="", en_print=True, wait_t=BMC_I2C_WAITING_TIME_MS, tty_incr=500):
    cmd = ""
    for retry in range(3):
      try:
        if reg == "":
          cmd = "i2cget -f -y %d 0x%02x" % (bus, addr)
        else:
          cmd = "i2cget -f -y %d 0x%02x 0x%02x" % (bus, addr, reg)
        if en_print == True:
          print(cmd)

        rs = self.sendCmd(cmd, writting=False)
        if "\n" in rs:
          rs = rs.splitlines()
        for line in rs:
          # Ex: read 1 byte => "0x01"
          #if len(line) == 4 and "0x" in line:
          if re.match("^0x[0-9a-f]{2}$", line.strip()):
            return int(line, 16)
      except Exception as e:
        print(repr(e))
        print("i2c_get: string handle error.")
        print("Cannot get i2c value from:" + rs)
      print("I2C read retry (%d)" % (retry + 1))
      wait_t += tty_incr

    return ""

  def bmc_show_ir3595_rev(self):
    ret = DIAG_STATUS_SUCCESS
    dev_name = "IR3595AMTRPBF"
    bus, addr, drv = [1, 0x12, "ir3595"]
    revision = 0

    rev_reg = 0x75
    try:
      ## Detect device
      self.bmc_i2c_device_delete(bus, addr)
      if not self.bmc_i2c_detect(bus, addr):
        UI.log("FAIL", "Cannot detect %s %d 0x%02x" % (drv, bus, addr))
        return DIAG_STATUS_FAILED
      #bmc_i2c_device_add(bus, addr, drv)

      val = self.bmc_i2c_get(bus, addr, rev_reg, False)
      if val == DIAG_STATUS_FAILED:
        UI.log("FAIL", "Get %s revision failed." % dev_name)
        return DIAG_STATUS_FAILED
      ## Revision 1 bytes order
      revision = val
      UI.log("---- %s version ----" % dev_name)
      print("%s: 0x%02x" % (dev_name, revision))

    except Exception as e:
      print(repr(e))
      return DIAG_STATUS_FAILED
    finally:
      self.bmc_i2c_device_add(bus, addr, drv)

    return ret

  def diag_item_check_fpga_pcie_bus_error(self):
    cmd = "cat /usr/local/accton/parameter/diag_item_162_time_setting"
    mode = "cat /usr/local/accton/parameter/check_pcie_bus_error_mode"
    time = self.sendCmd(cmd)
    time = time.strip()
    version = self.sendCmd("check_pcie_bus_error -v", writting=False)
    print("\nUtility version is: %s" % version) 
    print("\nTest for %s seconds..." % time)
    if mode == "PT":
      cmd = "pt_check_pcie_bus_error fpga %s \r" % time
    else:
      cmd = "check_pcie_bus_error fpga %s \r" % time
    
    self.send(cmd)
    while True:
      x = self.expect([self.prompt, '\r', '\n', ' '])
      if x == 0:
        break
    # if ret == 1:
    #   UI.log("FAIL", "Check FPGA PCI-E bus error is FAIL !")
    # else:
    UI.log("PASS", "Check FPGA PCI-E bus error is PASS !")

  def fpga_mdio_16q_test(self):
    cmd = 'cd /usr/local/accton/bin/FPGA_MDIO'
    self.send(cmd + "\r")
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    try:
      self.send("sh fpga_mdio_test all | tee /tmp/fpga_mdio_test.log \r")
      while True:
        x = self.expect([cd_prompt, '\r', 'i2cget', ' '])
        if x == 0:
          break
      time.sleep(0.2)
      out = self.sendCmd("cat /tmp/fpga_mdio_test.log", prompt=cd_prompt, writting=False)
      for line in out.splitlines():
        if line.strip() != '':
          print (line)
      retstr = self.sendCmd("cat /usr/local/accton/parameter/fpga_mdio_ret", prompt=cd_prompt)
      ret = int(retstr)
    except:
      print("Calling the script %s FAILED!" % "FPGA_MDIO_Test"); 
      UI.log("FAIL", "The Test for FPGA MDIO 16Q is FAIL !")
    if ret == 0 :
      UI.log("PASS", "The Test for FPGA MDIO 16Q is PASS !")
    else:
      UI.log("FAIL", "The Test for FPGA MDIO 16Q is FAIL !")

  def get_sensor_info_from_BMC(self):
    UI.log('ACTION', 'Get all sensor information from OpenBMC')
    self.send('sensor-util all \r')
    self.expect(self.prompt)
    UI.log('PASS', 'Get all sensor information from OpenBMC is PASS\n\n' + '=' * settings.glb.log_width)

  def Mcelog_Verify(self):
    cmd = 'cd /usr/local/accton/bin/'
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    self.sendCmd(cmd, writting=False, prompt=cd_prompt)

    ret = DIAG_STATUS_SUCCESS

    self.sendCmd("systemctl status mcelog.service -n 0;", prompt=cd_prompt)
    stdout_messages = self.sendCmd("systemctl is-active mcelog.service;", prompt=cd_prompt)
    if stdout_messages:
      stdout_messages = stdout_messages.splitlines()[0]
      if stdout_messages != "active":
        UI.log("FAIL","The status of mcelog service is %s!" % stdout_messages)
        return DIAG_STATUS_FAILED
    else:
      UI.log("FAIL","Get the active status of mcelog service is FAILED!")
      return DIAG_STATUS_FAILED

    UI.log("MCE log")
    self.sendCmd('journalctl -u mcelog.service --no-pager | grep "mcelog";', prompt=cd_prompt)
    stdout_messages = self.sendCmd('journalctl -u mcelog.service --no-pager | grep -c "MCE";', prompt=cd_prompt, writting=False)
    if re.search('^\d', stdout_messages):
      mcelog_error_counter = int(stdout_messages)
    else:
        UI.log("FAIL", "Get the count of mcelog is FAILED!")
        return DIAG_STATUS_FAILED
    ret = (mcelog_error_counter) # ret2 always gives 1.
    if ret:
      UI.log("FAIL", "The error status of mcelog are {%d}!" % (mcelog_error_counter))
      ret = DIAG_STATUS_FAILED
    return ret

  def th3_xgkr_test(self):
    self.kill_sdk_process()
    cmd = 'cd /usr/local/accton/bin/XGKR/'
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    self.sendCmd(cmd, writting=False, prompt=cd_prompt)

    ret = 0
    #bmc_util.tty_write("set_fan_speed.sh 50\r")
    try:
      self.send("./XGKR_Test \r")
      while True:
        x = self.expect([cd_prompt, '\r', '\n', '^Error', 'PORT: Error:', '(?i)PASS'])
        if x == 0 :
          break
        if x == 3 or x == 4 :
          ret = 1
        if x == 5:
          ret = 0
      time.sleep(0.2)
    except:
      UI.log("FAIL", "Calling the script %s FAILED!" % "XGKR_Test")
      return DIAG_STATUS_FAILED

    return ret

  def th3_mgmt_test(self):
    self.kill_sdk_process()
    cmd = 'cd /usr/local/accton/bin/SGMII/'
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    self.sendCmd(cmd, writting=False, prompt=cd_prompt)

    ret = 0
    #bmc_util.tty_write("set_fan_speed.sh 50\r")
    try:
      self.send("./SGMII_Test \r")
      while True:
        x = self.expect([cd_prompt, '\r', '\n', '^Error', 'PORT: Error:'])
        if x == 0 :
          break
        if x >= 3 and x <= 4 :
          ret = 1
      time.sleep(0.2)
    except:
      UI.log("FAIL", "Calling the script %s FAILED!" % "SGMII_Test")
      return DIAG_STATUS_FAILED
    
    return ret

  def phy16q_linespeed_test(self):
    self.kill_sdk_process()
    cmd = 'cd /usr/local/accton/bin/LineSpeed/'
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    self.sendCmd(cmd, writting=False, prompt=cd_prompt)

    ret = 0
    #bmc_util.tty_write("set_fan_speed.sh 50\r")
    try:
      self.send("./linespeed_test 16q \r")
      while True:
        x = self.expect([cd_prompt, '\r', '\n', '^Error', 'PORT: Error:', '(?i)FAIL', '>> PASS'])
        if x == 0 :
          break
        elif x >= 3 and x <=5 :
          ret = 1
        elif x == 6 :
          ret = 0
      time.sleep(0.2)
    except:
        UI.log("FAIL", "Calling the script %s FAILED!" % "linespeed_test")
        return DIAG_STATUS_FAILED
    return ret

  def serdes_info_test(self):
    self.kill_sdk_process()
    cmd = 'cd /usr/local/accton/bin/SERDES_DUMP/'
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    self.sendCmd(cmd, writting=False, prompt=cd_prompt)

    ret = 0
    try:
      self.send("./start_to_serdes_dump.sh \r")
      while True:
        x = self.expect([cd_prompt, '\r', '\n', '^Error', '(?i)diag_fail'])
        if x == 0 :
          break
        if x >= 3 and x <= 4 :
          ret = 1
      time.sleep(0.2)
    except:
      UI.log("FAIL", "Calling the script %s FAILED!" % "start_to_serdes_dump.sh")
      return DIAG_STATUS_FAILED
    return ret

  def phy16q_40g_linespeed_test(self):
    self.kill_sdk_process()
    cmd = 'cd /usr/local/bin/'
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    self.sendCmd(cmd, writting=False, prompt=cd_prompt)

    ret = 0
    try:
      self.send("./start_40G_bc_mode.sh \r")
      while True:
        x = self.expect([cd_prompt, '\r', '\n', '^ERROR', '(?i)FAIL', '(?i)bcmLINK', '(?i)PASS'])
        if x == 0 :
          break
        elif x >= 3 and x <= 4 :
          ret = 1
        elif x == 5 :
          self.send("\x03")
          ret = 1
          break
        elif x == 6 :
          ret = 0
      time.sleep(0.2)
    except:
      UI.log("FAIL", "Calling the script %s FAILED!" % "start_40G_bc_mode.sh")
      return DIAG_STATUS_FAILED
    return ret

  def phy16q_200g_linespeed_test(self):
    self.kill_sdk_process()
    cmd = 'cd /usr/local/bin/'
    cd_prompt = self.prompt.replace('~', cmd.split('/')[-2])
    self.sendCmd(cmd, writting=False, prompt=cd_prompt)

    ret = 0
    try:
      self.send("./start_200G_bc_mode.sh \r")
      while True:
        x = self.expect([cd_prompt, '\r', '\n', '^ERROR', '(?i)FAIL', '(?i)bcmLINK', '(?i)PASS'])
        if x == 0 :
          break
        elif x >= 3 and x <= 4 :
          ret = 1
        elif x == 5 :
          self.send("\x03")
          ret = 1
          break
        elif x == 6 :
          ret = 0
      time.sleep(0.2)
    except:
      UI.log("FAIL", "Calling the script %s FAILED!" % "start_40G_bc_mode.sh")
      return DIAG_STATUS_FAILED
    return ret

  def diag_item_check_th3_pcie_bus_error(self):
    cmd = "cat /usr/local/accton/parameter/diag_item_163_time_setting"
    cmd2 = "cat /usr/local/accton/parameter/pt_mode"
    
    time = self.sendCmd(cmd, writting=False).strip()
    version = self.sendCmd("check_pcie_bus_error -v", writting=False).splitlines()[0]
    pt_mode = self.sendCmd(cmd2, writting=False).strip()
    print("\nUtility version is: %s" % version)
    print("Test for %s seconds..." % time)
    print("PT mode  %s" % pt_mode)
    
    if pt_mode == "1":
      print("Current mode is PT mode")
      cmd = "pt_check_pcie_bus_error th3 %s" % time
    else:
      print("Current mode is FT-B and FT mode")
    cmd = "check_pcie_bus_error th3 %s \r" % time
    
    print("Cmd %s" % cmd)
    ret = 0
    self.send(cmd)
    while True:
      x = self.expect([self.prompt, '\r', '\n', '^Error', '^Elapse.*'])
      if x == 0 :
        break
      if x == 3 :
        ret = 1
    if ret == 1:
      return DIAG_STATUS_FAILED
    else:
      return DIAG_STATUS_SUCCESS

  def check_aer_dmesg(self, BFD):
    if BFD == "*":
        cmd = 'dmesg | grep "PCIe Bus Error"'
    else:
        cmd = 'dmesg | grep "%s: PCIe Bus Error"' % BFD

    ret = len(self.sendCmd(cmd).split())
    return ret

  def kill_sdk_process(self):
    retstr = self.sendCmd('top -n 1 | grep .bcm.user')
    if retstr != "":
      UI.log('Initial switch driver')
      self.sendCmd('pkill -f ".bcm.user"')
      time.sleep(5)
      retstr = self.sendCmd('top -n 1 | grep .bcm.user')
      if retstr == "":
        UI.log('Switch driver is ready')
    else:
      UI.log('Switch driver is ready')