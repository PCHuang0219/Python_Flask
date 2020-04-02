#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0660(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Erase the TH3 flash']
    purpose = ['To verify if the TH3 can be erase via spi.']
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
    UI.log('STEP#01', 'Set an IP for BMC eth0.')
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Erase TH3 via spi.')
      self.__TELNET.send('ls /tmp/\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('spi_util.sh erase spi1 TH3_FLASH\r')
      
      while True:
        if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Done.', 'OK.', 'done.'], timeout= 180) == 0:
          break
      
      self.__TELNET.send('wedge_power.sh reset -s\r')
      
      while True:
        if self.__TELNET.expect(['OpenBMC Release', 'minipack', 'Loading ', 'i2c ', 'gpio ', 'g_cdc ', ' '], timeout= 180) == 0:
          break
      
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('\r')
      time.sleep(60)
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sol.sh\r')
      
      if self.__TELNET.expect('quit', 'Checking') == 1:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': TH3 flash did not erased.')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': TH3 flash has erased.')
      
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0660 Erase_the_TH3_flash is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0660 Erase_the_TH3_flash is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
