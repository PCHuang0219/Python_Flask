#!/usr/bin/python3
####################################################################################################
"""
Module Name: system_4000.py
Purpose    : Execute system-4000 test case

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

class System_4000(Script):
  def __init__(self, dut, job_id = "", image_server = 'None'):
    headline = ['Traffic Test']

    purpose = ['Combine diagnostic test item :',
                '     108. Detecting machine check exceptions',
                '     400. Clear all AER mask of all pci devices',
                '     150. The Test of 10G KR CPU<-->TH3',
                '     151. The Test of 1G SGMII TH3<-->BCM5396',
                '     152. The Test of 16Q linespeed',
                '     154. Dump all serdes info',
                '     155. The Test of 16Q 40G linespeed',
                '     157. The Test of 16Q 200G linespeed',
                '     163. Check Tomahawk3 PCI-E bus error',
                '     401. Check if any AER error happened from dmesg',
                '     403. Check if any PCIE-Error happened from messages']

    self.__COMe = dut[0]
    self.__BMC = dut[1]

    self.__COMe_prompt = self.__COMe.ssh_credentials[5]
    self.__BMC_prompt = self.__BMC.ssh_credentials[5]
    super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
    super().beginLog()
    self.__pid = os.getpid()
    self.__thread_stop = False
    self.__COMe_SSH   = super().initUI(self.__COMe.ssh_credentials, self.__COMe.platform, System)
    self.__COMe_CHECK = super().initUI(self.__COMe.ssh_credentials, self.__COMe.platform, System)
    self.__BMC_SSH    = super().initUI(self.__BMC.ssh_credentials , self.__BMC.platform , System)
    self.__BMC_CHECK  = super().initUI(self.__BMC.ssh_credentials , self.__BMC.platform , System)

  def get_sensor_info_from_BMC(self):
    while not self.__thread_stop:
      if self.__BMC_CHECK.out_even and not self.__thread_stop:
        self.__BMC_CHECK.get_sensor_info_from_BMC()
        time.sleep(60)
        if not self.__thread_stop:
          break
  
  def run_swutil_show(self):
    while not self.__thread_stop:
      time.sleep(30)
      self.__COMe_CHECK.sendWithoutOutput('swutil show c > /dev/null & \n')
      return_val = False
      retry = 0
      pid = ""
      while retry < 3 and not return_val:
        self.__COMe_CHECK.sendWithoutOutput('jobs -p \n')
        ret = self.__COMe_CHECK.expect(self.__COMe_prompt, writting=False)
        if ret != 1:
          retstr = self.__COMe_CHECK.getBuff().splitlines()
          if re.search('^\d', retstr[1]):
            pid = retstr[1]
          else:                
            pid = retstr[1].split()[1]
          for line in retstr:
            if re.search('Done', line):
              return_val = True
              break
          if not return_val:
            time.sleep(5)
            retry += 1
        else:
          retry += 1
        
      if pid != "" and not return_val:
        self.__COMe_CHECK.sendWithoutOutput('kill -9 ' + pid + '\n')

  def run(self):
    sensor_p = Thread(target=self.get_sensor_info_from_BMC)
    sensor_p.start()

    # t = Thread(target=self.run_swutil_show)
    # t.start()

    time.sleep(5)

    remote_cmd = 'python /usr/local/accton/bin/diag_api.py %d normal 2>&1> /usr/local/accton/log/system_%d.log &'
    result_cmd = 'cat /usr/local/accton/log/system_%d.log'

    ### DIAG item : 108 ###
    UI.log("ACTION", "Detecting machine check exceptions")
    ret = self.__COMe_SSH.Mcelog_Verify()
    self.__COMe_SSH.sendCmd("cd", writting=False)
    if ret == DIAG_STATUS_FAILED:
      UI.log("FAIL", "Detecting machine check exceptions is FAIL")
    else:
      UI.log("PASS", "Detecting machine check exceptions is PASS")

    ### DIAG item : 400 ###
    UI.log('ACTION', 'Clear all AER mask of all pci devices START')
    ret = self.__COMe_SSH.pci_all_clear_all_aer_mask()
    if ret != 0:
      UI.log('FAIL', 'Clear all AER mask of all pci devices is FAIL !')
    else:
      UI.log('PASS', 'Clear all AER mask of all pci devices is PASS !')

    ### DIAG item : 150 ###
    UI.log("ACTION", "The Test of 10G KR CPU<-->TH3")
    ret = self.__COMe_SSH.th3_xgkr_test()
    self.__COMe_SSH.sendCmd("cd", writting=False)
    if ret == DIAG_STATUS_SUCCESS:
      UI.log("PASS", "The Test of 10G KR CPU<-->TH3 is PASS")
    else:
      UI.log("FAIL", "The Test of 10G KR CPU<-->TH3 is FAIL")

    ### DIAG item : 151 ###
    UI.log("ACTION", "The Test of 1G SGMII TH3<-->BCM5396")
    ret = self.__COMe_SSH.th3_mgmt_test()
    self.__COMe_SSH.sendCmd("cd", writting=False)
    if ret == DIAG_STATUS_SUCCESS:
      UI.log("PASS", "The Test of 1G SGMII TH3<-->BCM5396 is PASS")
    else:
      UI.log("FAIL", "The Test of 1G SGMII TH3<-->BCM5396 is FAIL")

    ### DIAG item : 152 ###
    UI.log("ACTION", "The Test of 16Q linespeed")
    ret = self.__COMe_SSH.phy16q_linespeed_test()
    self.__COMe_SSH.sendCmd("cd", writting=False)
    if ret == DIAG_STATUS_SUCCESS:
      UI.log("PASS", "The Test of 16Q linespeed is PASS")
    else:
      UI.log("FAIL", "The Test of 16Q linespeed is FAIL")

    ### DIAG item : 154 ###
    UI.log("ACTION", "Dump all serdes info")
    ret = self.__COMe_SSH.serdes_info_test()
    self.__COMe_SSH.sendCmd("cd", writting=False)
    if ret == DIAG_STATUS_SUCCESS:
      UI.log("PASS", "Dump all serdes info is PASS")
    else:
      UI.log("FAIL", "Dump all serdes info is FAIL")

    ### DIAG item : 155 ###
    UI.log("ACTION", "The Test of 16Q 40G linespeed")
    ret = self.__COMe_SSH.phy16q_40g_linespeed_test()
    self.__COMe_SSH.sendCmd("cd", writting=False)
    if ret == DIAG_STATUS_SUCCESS:
      UI.log("PASS", "The Test of 16Q 40G linespeed is PASS")
    else:
      UI.log("FAIL", "The Test of 16Q 40G linespeed is FAIL")

    # Wait R&D verify new eLoad
    # ### DIAG item : 157 ###
    # UI.log("ACTION", "The Test of 16Q 200G linespeed")
    # ret = self.__COMe_SSH.phy16q_200g_linespeed_test()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "The Test of 16Q 200G linespeed is PASS")
    # else:
    #   UI.log("FAIL", "The Test of 16Q 200G linespeed is FAIL")

    ### DIAG item : 163 ###
    UI.log("ACTION", "Check Tomahawk3 PCI-E bus error")
    ret = self.__COMe_SSH.diag_item_check_th3_pcie_bus_error()
    if ret == DIAG_STATUS_SUCCESS:
      UI.log("PASS", "Check Tomahawk3 PCI-E bus error is PASS")
    else:
      UI.log("FAIL", "Check Tomahawk3 PCI-E bus error is FAIL")

    ### DIAG item : 401 ###
    UI.log("ACTION", "Check if any AER error happened from dmesg")
    ret = self.__COMe_SSH.check_aer_dmesg("*")
    self.__COMe_SSH.sendCmd("cd", writting=False)
    if ret == DIAG_STATUS_SUCCESS:
      UI.log("PASS", "Check if any AER error happened from dmesg is PASS")
    else:
      UI.log("FAIL", "Check if any AER error happened from dmesg is FAIL")
    
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
    self.__thread_stop = True
    self.__COMe_SSH.close()
    self.__COMe_CHECK.close()
    self.__BMC_SSH.close()
    self.__BMC_CHECK.close()
    # Stop logging the script.
    super().endLog()
    os.kill(self.__pid, 9)
