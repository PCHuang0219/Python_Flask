#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0640(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Write the backup BIOS flash']
    purpose = ['To verify if the backup BIOS flash can be write via spi.']
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
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform, OpenBMC)
    self.__cycle = 1
    self.__fail_count = 0
    self.__backup_bios_filename = 'XG1_3A02.bin'

    # ==================================================================================================
    UI.log('STEP#01', 'Set an IP for BMC eth0.')
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy backup BIOS flash file to server.')
      server_file_path = self.image_server.local_old_image_path.replace(os.getcwd().replace('\\', '/'), '') + '/' + self.__backup_bios_filename
      
      UI.log('Backup BIOS version is ' + os.path.splitext(self.__backup_bios_filename)[0] + '.')
      
      self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/minipack_backup_bios.bin')
        
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Write backup BIOS flash image via spi.')
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('spi_util.sh write spi1 BACKUP_BIOS /var/tmp/minipack_backup_bios.bin\r')
      
      while True:
        if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Done.', 'OK.', 'done.', 'VERIFIED'], timeout= 180) == 0:
          break
      
      self.__TELNET.send('sol.sh\r')
      
      # SSH send wedge_power.sh reset off / on  to fix console server unable get message issue.
      self.__SSH.send('boot_info.sh bios reset slave\r')
      self.__SSH.expect(self.__dut.ssh_credentials[5])
      
      while True:
        if self.__TELNET.expect([']#', 'quit.', ']', 'IPv4.', 'IPv6.'], timeout= 180) == 0:
          break
      
      self.__TELNET.send('\r')
      self.__TELNET.expect(']#')
      self.__TELNET.send('version bios\r')
      self.__TELNET.expect(']#')
      
      result = re.search('(?i)' + os.path.splitext(self.__backup_bios_filename)[0], self.__TELNET.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The backup BIOS version is NOT match.')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The backup BIOS version is match.')
      
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('wedge_power.sh reset -s\r')
      
      while True:
        if self.__TELNET.expect(['OpenBMC Release', 'minipack', 'Loading', 'i2c', 'gpio', 'g_cdc'], timeout= 180) == 0:
          break
      
      time.sleep(40)
      
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0640 Write_the_backup_BIOS_flash is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0640 Write_the_backup_BIOS_flash is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
