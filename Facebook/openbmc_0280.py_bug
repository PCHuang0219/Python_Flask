#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0280(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Remote BIOS update']
    purpose = ['To verify if the BMC can upgrade COMe SPI booting flash via SPI bus.',
      'The following command can be used:',
      'root@bmc-oob:~# fw-util scm --update --bios <file path  e.g. /tmp/XG1_1A06.bin>']

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
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy BIOS image to BMC then check the image is transfer correctlly.')
      new_bios_ver = self.__TELNET.getImageVersion(self.image_server.local_new_image_path + '/BIOS/version.txt')
      new_bios_filename = self.__TELNET.getImageFilename(self.image_server.local_new_image_path + '/BIOS/version.txt')
      
      UI.log('COMeBIOS (' + new_bios_filename + ') New version is "' + new_bios_ver + '".')
      
      server_file_path = self.image_server.local_new_image_path.replace(self.image_server.local_root_path, '') + '/BIOS/' + new_bios_filename
      
      self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/minipack_COMe_BIOS.bin')
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use the command to update BIOS flash.')
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('fw-util scm --update --bios /var/tmp/minipack_COMe_BIOS.bin\r')
      
      while True:
        if self.__TELNET.expect([self.__dut.ssh_credentials[5], '%'], timeout= 180) == 0:
          break
      
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Reset the COM-e power and verify the version of BIOS in COM-e diag.')
      self.__TELNET.send('wedge_power.sh reset\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sol.sh\r')
      
      while True:
        if self.__TELNET.expect([']#', 'quit.', ']', 'IPv4.', 'IPv6.'], timeout= 180) == 0:
          break
      
      self.__TELNET.send('version bios\r')
      self.__TELNET.expect(']#')
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('fw-util scm --version\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)' + new_bios_ver, self.__TELNET.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BIOS version is NOT match!!')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BIOS version is match!!')
      
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0280 Remote_BIOS_update is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0280 Remote_BIOS_update is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
