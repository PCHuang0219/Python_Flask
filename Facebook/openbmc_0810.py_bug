#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0810(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Update bridge IC']
    purpose = ['None']

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
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Check the version of bridge IC.')
      self.__TELNET.send('fw-util scm --version | grep Bridge\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy bridge IC file to minipack then check the image is transfer correctlly.')
      new_bridge_ic_ver = self.__TELNET.getImageVersion(self.image_server.local_new_image_path + '/BIC/version.txt')
      new_bridge_ic_filename = self.__TELNET.getImageFilename(self.image_server.local_new_image_path + '/BIC/version.txt')
      
      server_file_path = self.image_server.local_new_image_path.replace(self.image_server.local_root_path, '') + '/BIC/' + new_bridge_ic_filename
      
      UI.log('Bridge IC(' + new_bridge_ic_filename + ') New version is "' + new_bridge_ic_ver + '".')
      
      self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/minipack_bic.bin')
        
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Write bridge IC via spi.')
      self.__TELNET.send('fw-util scm --update --bic /var/tmp/minipack_bic.bit\r')
      
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
      self.__TELNET.send('fw-util scm --version | grep Bridge\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)' + new_bridge_ic_ver, self.__TELNET.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Bridge_IC version is NOT match!!')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Bridge_IC version is match!!')
        
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0810 Update_Bridge_IC is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0810 Update_Bridge_IC is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
