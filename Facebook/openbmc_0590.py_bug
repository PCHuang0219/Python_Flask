#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0590(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Read the PIM1~8 phy1~ph4 EEPROM']
    purpose = ['To verify if the PIM1~8 phy1~4 EEPROM can be read via spi.']
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
    self.__phy_count = 4
    self.__fail_count = 0

    # ==================================================================================================
    UI.log('STEP#01', 'Set an IP for BMC eth0.')
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Read PIM PHY EEPROM via spi.')
      for pim_id in range(1, self.__pim_count + 1):
        for phy_id in range(1, self.__phy_count + 1):
          self.__TELNET.send('spi_util.sh read spi2 PIM' + str(pim_id) + ' PHY' + str(phy_id)  + '_EE /var/tmp/read_pim' + str(pim_id) + '_phy' + str(phy_id) + '\r')
          
          while True:
            if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Done.'], timeout= 180) == 0:
              break
            
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy BCM5396 EEPROM file to server.')
      for pim_id in range(1, self.__pim_count + 1):
        for phy_id  in range(1, self.__phy_count +1):
          server_file_path = self.image_server.local_read_file_path.replace(self.image_server.local_root_path, '') + '/pim' + str(pim_id) + '_phy' + str(phy_id) + '_ee'
          
          self.__fail_count += self.__TELNET.uploadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
            server_file_path, '/var/tmp/read_pim' + str(pim_id) + '_phy' + str(phy_id))
          
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0590 Read_the_PIM1~8_phy1~4_EEPROM is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0590 Read_the_PIM1~8_phy1~4_EEPROM is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
