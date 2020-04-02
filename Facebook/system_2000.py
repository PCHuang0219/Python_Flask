#!/usr/bin/python3
####################################################################################################
"""
Module Name: system_2000.py
Purpose    : Execute system-2000 test case

Description:
  There are two necessary parameter :
            - dut            : the DUT object on which testing is performed.
            - job_id          : ID of the testcase under the job.

History     :
    Anber Huang 12/20/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.system import System
from lib.cli.facebook.parameters import *
from multiprocessing import Process
from threading import Thread
import time
import os
import re

class System_2000(Script):
  def __init__(self, dut, job_id = "", image_server = 'None'):
    headline = ['FPGA / I2C Test']

    purpose = ['Stress FPGA with both path low speed path & high speed path',
                'Combine diagnostic test item :',
                '     115. Show Revision of CPLD and FPGA',
                '     400. Clear all AER mask of all pci devices',
                '     158. The Test for FPGA I2C Low-Speed Path QSFP EEPROM',
                '     159. The Test for FPGA I2C High-Speed Path',
                '     403. Check if any PCIE-Error happened from messages']

    self.__COMe = dut[0]
    self.__BMC = dut[1]

    self.__COMe_prompt = self.__COMe.ssh_credentials[5]
    self.__BMC_prompt = self.__BMC.ssh_credentials[5]
    super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
    super().beginLog()
    self.__pid = os.getpid()
    self.__thread_stop = False
    self.__COMe_SSH = super().initUI(self.__COMe.ssh_credentials, self.__COMe.platform, System)
    self.__BMC_SSH  = super().initUI(self.__BMC.ssh_credentials , self.__BMC.platform , System)
    self.__BMC_CHECK= super().initUI(self.__BMC.ssh_credentials , self.__BMC.platform , System)

  def get_sensor_info_from_BMC(self):
    while not self.__thread_stop:
      if self.__BMC_CHECK.out_even and not self.__thread_stop:
        self.__BMC_CHECK.get_sensor_info_from_BMC()
        time.sleep(60)
        if not self.__thread_stop:
          break

  def run(self):
    sensor_p = Thread(target=self.get_sensor_info_from_BMC)
    sensor_p.start()

    time.sleep(5)

    remote_cmd = 'python /usr/local/accton/bin/diag_api.py %d normal 2>&1> /usr/local/accton/log/system_%d.log &'
    result_cmd = 'cat /usr/local/accton/log/system_%d.log'

    ### DIAG item : 115 ###
    UI.log('ACTION', 'Show Revision of CPLD and FPGA START')
    ret = DIAG_STATUS_SUCCESS
    rs = ""
    try:
      cpld_ls = {}
      fpga_ls = {}
      others_ls = {}
      board_cfg = self.__COMe_SSH.get_board_config()
      if board_cfg & BOARD_SMB:
        cpld_ls["SMBCPLD"] = ret
        fpga_ls["IOBFPGA"] = ret
        if board_cfg & BOARD_PT:
          pass
        else:
          others_ls["POWR1220AT8"] = self.__BMC_SSH.bmc_show_powr1220_rev()
          others_ls["IR3595AMTRPBF"] = self.__BMC_SSH.bmc_show_ir3595_rev()
      if board_cfg & BOARD_SCM:
        cpld_ls["SCMCPLD"] = ret
      if board_cfg & BOARD_FCM_ALL:
        cpld_ls["Top FCMCPLD"] = ret
        cpld_ls["Bottom FCMCPLD"] = ret
      if board_cfg & BOARD_PDB_ALL:
        cpld_ls["Left PDBCPLD"] = ret
        cpld_ls["Right PDBCPLD"] = ret
      if board_cfg & BOARD_PIM_ALL:
        pim_ls = [PIM_ID_TO_NUM[brd_id] for brd_id in PIM_ID_TO_NUM if brd_id & board_cfg]
        for pim_num in pim_ls:
          fpga_ls["PIM %d DOMFPGA" % pim_num] = ret

      fail_str_ls = ["read error", "0.0", "255.255", "Read failed", "not detected", "not inserted"]

      ## Check cpld version ##
      for retry in range(4):
        if len(cpld_ls) == 0:
          break
        exist_fail = False
        if retry > 0:
          print("cpld retry %d" % retry)
        rs = self.__BMC_SSH.get_process_result("cpld_ver.sh")
        UI.log("------CPLD version------")
        for line in rs:
          for cpld_name in cpld_ls:
            if cpld_name in line:
              print(line)
              ## Check error message ##
              for err in fail_str_ls:
                if err in line:
                  cpld_ls[cpld_name] = DIAG_STATUS_FAILED
                  exist_fail = True
                else:
                  exist_fail = False
        if exist_fail:
          continue
        else:
          break
      
      ## Check fpga version ##
      for retry in range(4):
        if len(fpga_ls) == 0:
          break
        exist_fail = False
        check_next_line = False
        last_fpga_name = ""
        rs = self.__BMC_SSH.get_process_result("fpga_ver.sh")
        if retry > 0:
          UI.log("Get FPGA Version %d times" % (retry + 1))
        else:
          UI.log("Get FPGA Version first times")
        for line in rs:
          if "FPGA" in line and "-----" in line:
            print(line)
          elif "IOBFPGA" in line:
            print(line)
            for err in fail_str_ls:
              if err in line:
                fpga_ls["IOBFPGA"] = DIAG_STATUS_FAILED
                exist_fail = True
          elif re.match("PIM [1-8]:", line):
            pim_str = line.split(":")[0]
            for name in fpga_ls:
              if pim_str in name:
                print(line)
                check_next_line = True
                last_fpga_name = name
                break
          elif "DOMFPGA" in line and check_next_line:
            print(line)
            check_next_line = False
            for err in fail_str_ls:
              if err in line:
                fpga_ls[last_fpga_name] = DIAG_STATUS_FAILED
                exist_fail = True
                break
          
        if exist_fail:
          continue
        else:
          break
        
      ret = 0
      ## Examine result ##
      for ls in [others_ls, cpld_ls, fpga_ls]:
        for item in ls:
          if ls[item] is not DIAG_STATUS_SUCCESS:
            UI.log("FAIL", "%s: get version fail !" % item)
            ret = -1
      if ret == 0:
        UI.log("PASS", "Show Revision of CPLD and FPGA is PASS")
      else:
        UI.log("FAIL", "Show Revision of CPLD and FPGA is FAIL")

    except Exception as e:
      print(repr(e))
      print(rs)
      UI.log('FAIL', 'Show Revision of CPLD and FPGA is FAIL')

    ### DIAG item : 400 ###
    UI.log('ACTION', 'Clear all AER mask of all pci devices START')
    ret = self.__COMe_SSH.pci_all_clear_all_aer_mask()
    if ret != 0:
      UI.log('FAIL', 'Clear all AER mask of all pci devices is FAIL !')
    else:
      UI.log('PASS', 'Clear all AER mask of all pci devices is PASS !')

    
    ### DIAG item : 159 ###
    UI.log('ACTION', 'The Test for FPGA I2C High-Speed Path START')
    retstr = self.__COMe_SSH.sendCmd('python /usr/local/accton/bin/diag_api.py 159 normal', timeout=60)
    if retstr != "" :
      retstr = retstr.splitlines()
      if "PASS" in  retstr[-2]:
        UI.log('PASS', 'The Test for FPGA I2C High-Speed Path is PASS !')
      else:
        UI.log('FAIL', 'The Test for FPGA I2C High-Speed Path is FAIL !')
    else:
      UI.log('FAIL', 'The Test for FPGA I2C High-Speed Path is FAIL !')
    
    ### DIAG item : 158 ###
    UI.log('ACTION', 'The Test for FPGA I2C Low-Speed Path QSFP EEPROM START')
    retstr = self.__COMe_SSH.sendCmd('python /usr/local/accton/bin/diag_api.py 158 normal', timeout=300)
    if retstr != "" :
      retstr = retstr.splitlines()
      if "PASS" in  retstr[-2]:
        UI.log('PASS', 'The Test for FPGA I2C Low-Speed Path QSFP EEPROM is PASS !')
      else:
        UI.log('FAIL', 'The Test for FPGA I2C Low-Speed Path QSFP EEPROM is FAIL !')
    else:
      UI.log('FAIL', 'The Test for FPGA I2C Low-Speed Path QSFP EEPROM is FAIL !')


    # ### Wait DIAG item : 158 finished ###
    # while True:
    #   retstr = self.__COMe_SSH.sendCmd('jobs -p', writting=False)
    #   if retstr != "":
    #     retstr = retstr.splitlines()
    #     for line in retstr:
    #       if not re.search('^\d', line):
    #         UI.log('The Test for FPGA I2C Low-Speed Path QSFP EEPROM RESULT')
    #         rs = self.__COMe_SSH.sendCmd(result_cmd % 158)
    #         if rs != "":
    #           rs = rs.splitlines()
    #           if "PASS" in rs[-2]:
    #             UI.log("PASS", "The Test for FPGA I2C Low-Speed Path QSFP EEPROM is PASS")
    #           else:
    #             UI.log("FAIL", "The Test for FPGA I2C Low-Speed Path QSFP EEPROM is FAIL")
    #         else:
    #           UI.log("FAIL", "The Test for FPGA I2C Low-Speed Path QSFP EEPROM is FAIL")
    #         break_val = True
    #         break
    #   if break_val:
    #     break
    
    ### DIAG item : 403 ###
    UI.log('ACTION', 'Check CPU FPGA pcie error START')
    ret = self.__BMC_SSH.bmc_check_pcie_err()
    if ret == DIAG_STATUS_FAILED:
      UI.log("FAIL", "Check BMC system event log is FAIL !")
    else:
      UI.log("PASS", "Check BMC system event log is PASS !")

    ret = self.__COMe_SSH.check_cpu_log()
    if ret == DIAG_STATUS_FAILED:
      UI.log("FAIL", "Check CPU FPGA pcie error is FAIL !")
    else:
      UI.log("PASS", "Check CPU FPGA pcie error is PASS !")

    self.__thread_stop = True

  def stop(self):
    self.__COMe_SSH.close()
    self.__BMC_SSH.close()
    self.__BMC_CHECK.close()
    # Stop logging the script.
    super().endLog()
    os.kill(self.__pid, 9)
    