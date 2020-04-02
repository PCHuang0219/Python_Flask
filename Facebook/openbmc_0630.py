#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0630(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Erase the backup BIOS flash']
    purpose = ['To verify if the backup BIOS flash can be erase via spi.']
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
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Erase backup BIOS flash via spi.')
      self.__TELNET.send('spi_util.sh erase spi1 BACKUP_BIOS\r')
      
      while True:
        if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Done.', '.', 'done.'], timeout= 180) == 0:
          break
      
      self.__TELNET.send('echo 1 > /sys/class/i2c-adapter/i2c-2/2-0035/iso_buff_brg_com_bios_dis0_n\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('wedge_power.sh reset\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sol.sh\r')
      
      try:
        if self.__TELNET.expect([']#', 'quit.', ']', 'IPv4.', 'IPv6.'], timeout= 180) == 0:
          self.__fail_count += 1
          
          break
      except:
        break
      
      if self.__fail_count  == 0:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Backup_bios has erased!!')
      else:
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Backup_bios did not erase!!')
      
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('echo 0 > /sys/class/i2c-adapter/i2c-2/2-0035/iso_buff_brg_com_bios_dis0_n\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0630 Erase_the_backup_BIOS_flash is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0630 Erase_the_backup_BIOS_flash is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
