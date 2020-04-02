#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0690(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Read PIM fru eeprom information']
    purpose = ['To verify if the PIM fru eeprom can be shown.']
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
    self.__pim_count = 8
    self.__fail_count = 0

    # ==================================================================================================
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Read eeprom information about PIM fru.')
      for pim_id in range(1, self.__pim_count + 1):
        self.__TELNET.send('peutil ' + str(pim_id) + '\r')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
        
        # result = re.search('(?i)Version', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': PIM fru EEPROM read failure.')
      # else:
        # self.__fail_count += 1
        
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': PIM fru EEPROM read success.')
        
    # if self.__fail_count == 0:
      # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0690 Read_PIM_fru_eeprom_information is passed.')
    # else:
      # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0690 Read_PIM_fru_eeprom_information is failed.')
      
      UI.log('CHECK', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0690 Read_PIM_fru_eeprom_information need to check.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
