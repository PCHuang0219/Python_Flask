#!/usr/bin/python3
####################################################################################################
"""
Module Name: system_1000.py
Purpose    : Execute system-1000 test case

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
from threading import Thread
import time
import os
import re

class System_1000(Script):
  def __init__(self, dut, job_id = "", image_server = 'None'):
    headline = ['CPU/Memory Test']

    purpose = ['Combine diagnostic test item :',
                '      54. Show COM-E HW information',
                '      11. The R/W test for memory device(RAM)',
                '      63. The stress-ng performance test for CPU',
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
    self.__COMe_SSH_1 = super().initUI(self.__COMe.ssh_credentials, self.__COMe.platform, System)
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
    ### diag 54 ###
    UI.log('ACTION', 'Show COM-E HW information START')
    try:
      dmistr = self.__COMe_SSH.sendCmd("dmidecode -t 0 -t 1 -t 2 -t 3 -t 4 -t 17")
    except Exception as e:
      UI.log("FAIL", "dmidecode(%d): FAIL!" % e.returncode)
    try:
      smartstr = self.__COMe_SSH.sendCmd("smartctl -i /dev/sda -d sat")
    except Exception as e:
      UI.log("FAIL", "smartctl(%d): FAIL!" % e.returncode)

    rs = cmd = bic_ver = pvccin_vr = ddrab_vr = p1v05_vr = ''
    try:
      cmd = 'fw-util scm --version'
      rs = self.__BMC_SSH.bmc_check_process_done(cmd, 1, 15, True, 3)
      assert rs[0] == DIAG_STATUS_SUCCESS
      bicstr_ls = rs[1].splitlines()
      assert len(bicstr_ls) > 4
      for line in bicstr_ls:
        if 'Bridge-IC Version' in line:
          bic_ver = line.split(':')[1].strip()
        elif 'PVCCIN VR Version' in line:
          pvccin_vr = line.split(':')[1].strip()
        elif 'DRAB VR Version' in line:
          ddrab_vr = line.split(':')[1].strip()
        elif 'P1V05 VR Version' in line:
          p1v05_vr = line.split(':')[1].strip()
    except AssertionError:
      print('%s FAIL!' % cmd)
      print('Debug:' + str(rs))
      UI.log("FAIL", "AssertionError")
    except Exception as e:
      UI.log("FAIL", "Exception : " + str(e))

    try:
      cmd = 'bic-util scm --read_fruid'
      rs = self.__BMC_SSH.bmc_check_process_done(cmd, 1, 15, True, 3)
      assert rs[0] == DIAG_STATUS_SUCCESS
      rs_ls = rs[1].splitlines()
      assert len(rs_ls) > 21
      UI.log("Print Hardware Information Start")
      for line in rs_ls:
        if ':' in line and 'root@' not in line:
          print(line)
    except AssertionError:
      print('%s FAIL!' % cmd)
      print('Debug:' + str(rs))
      UI.log("FAIL", "AssertionError")
    except Exception as e:
      UI.log("FAIL", "Exception : " + str(e))


    dmi = dmistr.splitlines()
    smart = smartstr.splitlines()
    #ecver = ecverstr.splitlines()

    for anchor, line in enumerate(dmi):
      if "BIOS Information" in line:
        break
    print("BIOS Vender               : %s" % parse_value(dmi[anchor+1]))
    print("BIOS Revision             : %s" % parse_value(dmi[anchor+2]))
    print("BIOS FW Revision          : %s" % parse_value(dmi[anchor+27]))
    print("BIC Version               : %s" % bic_ver)
    print("PVCCIN VR Version         : %s" % pvccin_vr)
    print("DDRAB VR Version          : %s" % ddrab_vr)
    print("P1V05 VR Version          : %s" % p1v05_vr)


    for anchor, line in enumerate(dmi):
      if "System Information" in line:
        break

    print("Manufacturer              : %s" % parse_value(dmi[anchor+1]))
    print("Product Name              : %s" % parse_value(dmi[anchor+2]))
    #print("Version                  : %s" % parse_value(dmi[anchor+3]))
    #print("Serial Number            : %s" % parse_value(dmi[anchor+4]))
    #print("Minilake SN              : %s" % snstr[16])
    #print("SKU Number               : %s" % parse_value(dmi[anchor+7]))
    #print("Family                   : %s" % parse_value(dmi[anchor+8]))

    for anchor, line in enumerate(dmi):
      if "Base Board Information" in line:
        break

    #print("Base Board SN            : %s" % parse_value(dmi[anchor+4]))

    for anchor, line in enumerate(dmi):
      if "Chassis Information" in line:
        break

    #print("Chassis Manufacturer     : %s" % parse_value(dmi[anchor+1]))
    #print("Chassis Serial Number    : %s" % parse_value(dmi[anchor+5]))
    #print("Chassis Asset Tag        : %s" % parse_value(dmi[anchor+6]))

    for anchor, line in enumerate(dmi):
      if "Processor Information" in line:
        break

    print("CPU Manufacturer          : %s" % parse_value(dmi[anchor+4]))
    print("CPU Version               : %s" % parse_value(dmi[anchor+36]))
    print("CPU Clock                 : %s" % parse_value(dmi[anchor+38]))
    print("CPU Number of Cores       : %s" % parse_value(dmi[anchor+49]))
    print("CPU Max Speed             : %s" % parse_value(dmi[anchor+39]))

    for anchor, line in enumerate(dmi):
      if "DMI type 17, 40 bytes" in line:
#        if "Memory Device" in line:
        break

    print("DIMM_A0 Size              : %s" % parse_value(dmi[anchor+6]))
    print("DIMM_A0 Factor            : %s" % parse_value(dmi[anchor+7]))
    print("DIMM_A0 Type              : %s" % parse_value(dmi[anchor+11]))
    print("DIMM_A0 Speed             : %s" % parse_value(dmi[anchor+13]))
    print("DIMM_A0 Manufacturer      : %s" % parse_value(dmi[anchor+14]))
    print("DIMM_A0 SN                : %s" % parse_value(dmi[anchor+15]))
    print("DIMM_A0 PN                : %s" % parse_value(dmi[anchor+17]))

    for anchor, line in enumerate(dmi):
      if "DMI type 17, 40 bytes" in line:
#        if "Memory Device" in line:
        break

    print("DIMM_B0 Size              : %s" % parse_value(dmi[anchor+30]))
    print("DIMM_B0 Factor            : %s" % parse_value(dmi[anchor+31]))
    print("DIMM_B0 Type              : %s" % parse_value(dmi[anchor+35]))
    print("DIMM_B0 Speed             : %s" % parse_value(dmi[anchor+37]))
    print("DIMM_B0 Manufacturer      : %s" % parse_value(dmi[anchor+38]))
    print("DIMM_B0 SN                : %s" % parse_value(dmi[anchor+39]))
    print("DIMM_B0 PN                : %s" % parse_value(dmi[anchor+41])) 

    for anchor, line in enumerate(smart):
      if "Device Model" in line:
        break

    print("SSD Vender                : %s" % parse_value(smart[anchor]))
    print("SSD SN                    : %s" % parse_value(smart[anchor+1]))
    print("SSD FW Version            : %s" % parse_value(smart[anchor+3]))

    UI.log("PASS", "Show COM-E HW information is PASS !")
    
    ### DIAG item : 11 ###
    UI.log('ACTION', 'The R/W test for memory device(RAM) START IN BACKGROUND')
    self.__COMe_SSH.sendCmd(remote_cmd % (11, 11))

    ### DIAG item : 63 ###
    UI.log('ACTION', 'The stress-ng performance test for CPU START')
    self.__COMe_SSH.cpu_stress_ng_test()

    ### Wait DIAG item : 11 finished ###
    while True:
      retstr = self.__COMe_SSH.sendCmd('jobs -p', writting=False)
      if retstr == "" :
        UI.log('The R/W test for memory device(RAM) RESULT')
        self.__COMe_SSH.sendCmd(result_cmd % 11)
        break
    
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
