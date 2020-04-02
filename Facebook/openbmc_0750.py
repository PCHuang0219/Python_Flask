#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0750(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Downgrade BMC flash']
    purpose = ['scp downgrade_flash-minipack root@<bmc-ip-addr>:/tmp',
      'flashcp -v flash-minipack /dev/mtd5',
      'Then, reboot the system for the downgrade firmware to take effect.']
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
    self.__minipack_ver = 'OpenBMC Release minipack-v1.9'
    self.__minipack_filename = 'flash-minipack_v1_9'

    # ==================================================================================================
    UI.log('STEP#01', 'Set an IP for BMC eth0.')
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Show the openBMC version.')
      self.__TELNET.send('cat /etc/issue\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy downgrade_flash-minipack file to minipack then check the image is transfer correctlly.')
      server_file_path = self.image_server.local_old_image_path.replace(os.getcwd().replace('\\', '/'), '') + '/' + self.__minipack_filename
      
      UI.log('Minipack version is ' + os.path.splitext(self.__minipack_filename)[0] + '.')
      
      self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/minipack_down_flash')
        
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Downgrade BMC flash and power reset when after writting.')
      self.__TELNET.send('flashcp -v /var/tmp/minipack_down_flash /dev/mtd5\r')
      
      while True:
        if self.__TELNET.expect([self.__dut.ssh_credentials[5], '%'], timeout= 180) == 0:
          break
      
      self.__TELNET.send('wedge_power.sh reset -s\r')
      
      while True:
        if self.__TELNET.expect(['OpenBMC Release', 'minipack', 'Loading', 'i2c', 'gpio', 'g_cdc'], timeout= 180) == 0:
          break
      
      time.sleep(40)
      
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cat /etc/issue\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)' + self.__minipack_ver, self.__TELNET.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': OpenBmc version is NOT match!!')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': OpenBmc version is match!!')
        
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0750 Downgrade_BMC_flash is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0750 Downgrade_BMC_flash is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
