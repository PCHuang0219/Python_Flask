#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0580(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Erase the 5 port switch(BCM5396)']
    purpose = ['To verify if the BCM5396 EEPROM can be erase via spi.']
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
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Erase BCM5396 EEPROM via spi.')
      self.__TELNET.send('spi_util.sh erase spi1 BCM5396_EE\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5], timeout= 180)
      
      if re.search('(?i)Done', self.__TELNET.getBuff(), re.M) == None:
        self.__fail_count += 1
    
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0580 Erase_the_5_port_switch_BCM5396 is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0580 Erase_the_5_port_switch_BCM5396 is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
