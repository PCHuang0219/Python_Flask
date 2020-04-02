#!/usr/bin/python3
####################################################################################################

import re
import os
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0080(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['External BIOS flash chip to boot COMe']
    purpose = ['To verify if COMe can be booted by external BIOS flash chip.']

    self.__dut = dut[1]
    self.image_server = image_server
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform, OpenBMC)
    self.__cycle = 1
    self.__fail_count = 0
    self.__backup_bios_filename = 'XG1_3A02.bin'

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Set an IP for BMC eth0.')
      self.__SSH.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + ' \r')
      self.__SSH.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy BIOS image to BMC then check the image is transfer correctlly.')
      server_file_path = self.image_server.local_old_image_path.replace(os.getcwd().replace('\\', '/'), '') + '/' + self.__backup_bios_filename
        
      UI.log('Backup BIOS version is ' + os.path.splitext(self.__backup_bios_filename)[0] + '.')
      
      self.__SSH.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/minipack_backup_bios.bin')
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use the BIOS which the version is different from using to upgrade backup BIOS flash.')
      self.__SSH.send('sv stop mTerm\r')
      self.__SSH.expect(self.__dut.ssh_credentials[5])
      self.__SSH.send('spi_util.sh write spi1 BACKUP_BIOS /var/tmp/minipack_backup_bios.bin\r')
      
      while True:
        if self.__SSH.expect([self.__dut.ssh_credentials[5], 'Done.', 'OK., ''done.', 'VERIFIED'], timeout= 180) == 0:
          break
          
      self.__SSH.send('boot_info.sh bios reset slave\r')
      self.__SSH.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'To accessed by using serial over LAN')
      self.__SSH.send('sol.sh\r')
      
      while True:
        if self.__SSH.expect([']#', 'quit.', ']', 'IPv4.', 'IPv6.'], timeout= 180) == 0:
          break
      
      self.__SSH.send('\r')
      self.__SSH.expect(']#')
      
      # ==================================================================================================
      UI.log('STEP#05 - cycle#' + str(i) + '/' + str(self.__cycle), 'use the command to show BIOS version in Diag.')
      self.__SSH.send('version bios\r')
      self.__SSH.expect(']#')
      
      result = re.search('(?i)' + os.path.splitext(self.__backup_bios_filename)[0], self.__SSH.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The backup BIOS version is NOT match.')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The backup BIOS version is match.')
      
      self.__SSH.send('\x18')
      self.__SSH.expect(self.__dut.ssh_credentials[5])
      self.__SSH.send('wedge_power.sh reset -s\r')
      
      while True:
        if self.__SSH.expect(['OpenBMC Release', 'minipack', 'Loading', 'i2c', 'gpio', 'g_cdc'], timeout= 180) == 0:
          break
      
      self.__SSH.send('\r')
      self.__SSH.expect('login:')
      self.__SSH.send(self.__dut.ssh_credentials[3] + '\r')
      self.__SSH.expect('Password:')
      self.__SSH.send(self.__dut.ssh_credentials[4] + '\r')
      self.__SSH.expect(self.__dut.ssh_credentials[5])

    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0080 External_BIOS_flash_chip_to_boot_COMe is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0060 External_BIOS_flash_chip_to_boot_COMe is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()