#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0820(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Read FAN tray FCM fru eeprom information']
    purpose = ['None']

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
    self.__pim_count = 8

    # ==================================================================================================
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      self.__TELNET.send('feutil all\r')
        
      while True:
        if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Fan'], timeout= 180) == 0:
          break
        
      UI.log('CHECK', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The FCM fru/FAN tray eeprom read complete.')
        
    UI.log('CHECK', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0820 Reading_PSU_information need to check.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
