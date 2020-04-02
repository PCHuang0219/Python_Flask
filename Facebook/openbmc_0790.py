#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0790(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Boot up with backup BMC']
    purpose = ['To verify if system can be booted by backup BMC chip.']
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
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Show the openBMC version .')
      self.__TELNET.send('cat /etc/issue\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
        
      self.__openbmc_ver = re.search('(?i)OpenBMC Release minipack-(.*)\n', self.__TELNET.getBuff(), re.M)
        
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Boot up BMC via backup BMC chip.')
      self.__TELNET.send('/usr/local/bin/openbmc-utils.sh\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('devmem_set_bit $(scu_addr 70) 17\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('devmem 0x1e785024 32 0x00989680\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('devmem 0x1e785028 16 0x4755\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('devmem 0x1e78502c 8 0xB3\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
        
      while True:
        if self.__TELNET.expect(['OpenBMC Release ', 'minipack', ' ', '\r', 'gpio', 'g_cdc'], timeout= 180) == 0:
          break
        
      time.sleep(40)
        
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Show the openBMC version is different from the step S1. to confirm that the BMC chip is boot up by the other one.')
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
        
      result = re.search('(?i)OpenBMC Release minipack-' + self.__openbmc_ver.group(1) + '\n', self.__TELNET.getBuff(), re.M)
        
      if result == None:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Bootup on backup BIOS success.')
      else:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': OpenBMC shall be bootup on backup BIOS.')
        
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('wedge_power.sh reset -s\r')
        
      while True:
        if self.__TELNET.expect(['OpenBMC Release ', self.__dut.ssh_credentials[5], 'minipack', 'Loading', 'i2c', 'gpio', 'g_cdc'], timeout= 180) == 0:
          break
        
      time.sleep(40)
        
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])

    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0790 Boot_up_with_backup_BMC is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0790 Boot_up_with_backup_BMC is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
