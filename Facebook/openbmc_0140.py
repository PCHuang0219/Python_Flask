#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0140(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Reading SMB fru eeprom information']
    purpose = ['To verify Wedge system EEPROM can be dumped with the BMC utility "weutil" successfully.']

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
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Verify the information of wedge system EEPROM can be read with the command.')
      self.__TELNET.send('weutil\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])

      result = re.search('(?i)Failed', self.__TELNET.getBuff(), re.M)

      if result == None:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The SMB fru eeprom read complete.')
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0140 Reading_SMB_fru_eeprom_information is passed.')
      else:
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The SMB fru eeprom read failed.')
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0140 Reading_SMB_fru_eeprom_information is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
