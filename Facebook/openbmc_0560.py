#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0560(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Read the 5 port switch(BCM5396)']
    purpose = ['To verify if the BCM5396 EEPROM can be read via spi.']
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
      UI.log('STEP#02', 'Read BCM5396 EEPROM via spi.')
      self.__TELNET.send('ls /tmp/\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('spi_util.sh read spi1 BCM5396_EE /var/tmp/read_bcm5396_ee.bin\r')
      
      while True:
        if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Done.'], timeout= 180) == 0:
          break
          
      # ==================================================================================================
      UI.log('STEP#03', 'Use scp funtion to copy BCM5396 EEPROM file to server.')
      server_file_path = self.image_server.local_read_file_path.replace(self.image_server.local_root_path, '') + '/read_bcm5396_ee.bin'
        
      self.__fail_count += self.__TELNET.uploadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/read_bcm5396_ee.bin')
    
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0560 Read_the_5_port_switch_BCM5396 is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0560 Read_the_5_port_switch_BCM5396 is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
