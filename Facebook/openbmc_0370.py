#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0370(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Checking SMB CPLD, SCM CPLD, FCM CPLD version']
    purpose = ['To check the CPLD version of all mould.', 
                'The following command can be used:', 
                '   "root@bmc-oob:~# cpld_ver.sh"']

    self.__dut = dut[1]
    self.image_server = image_server
    super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__TELNET = super().initUI(self.__dut.telnet_credentials, self.__dut.platform, OpenBMC)
    self.__cycle = 1
    self.__fail_count = 0
   # ==================================================================================================
    self.__TELNET.sendCmd('cpld_ver.sh')
           
    if self.__fail_count == 0:
      UI.log('PASS', 'BMC_0370 Checking SMB CPLD, SCM CPLD, FCM CPLD version is passed.')
    else:
      UI.log('FAIL', 'BMC_0370 Checking SMB CPLD, SCM CPLD, FCM CPLD version is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
