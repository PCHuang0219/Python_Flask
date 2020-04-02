#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0350(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Upgrade CPLD for PIM']
    purpose = ['To verify if the CPLD of PIM Module can be Upgrade by BMC.']

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
    self.__fail_count = 0
    self.__pim_mux_check_fileanme = 'pim_mux_check.vme'
    # ==================================================================================================
    UI.log('STEP#01', 'Set an IP for BMC eth0.')
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy PIM update image to BMC then check the image is transfer correctlly.')
      new_pim_spi_mux_ver = self.__TELNET.getImageVersion(self.image_server.local_new_image_path + '/16Q/PIMSPIMUX/version.txt')
      new_pim_spi_mux_filename = self.__TELNET.getImageFilename(self.image_server.local_new_image_path + '/16Q/PIMSPIMUX/version.txt')
      
      UI.log('PIMSPIMUX (' + new_scm_cpld_filename + ') New version is "' + new_pim_spi_mux_ver + '".')
      
      server_file_path = self.image_server.local_new_image_path.replace(self.image_server.local_root_path, '') + '/16Q/PIMSPIMUX/' + new_fcm_cpld_filename
      
      self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/minipack_pim_cpld.vme')
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use the command to update PIM update CPLD.')
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      for pim_id in range(1, self.__pim_count + 1):
        self.__TELNET.send('spimcpld_update.sh ' + str(pim_id) + ' /var/tmp/minipack_pim_cpld.vme\r')
        
        while True:
          if self.__TELNET.expect([self.__dut.ssh_credentials[5], '%'], timeout= 180) == 0:
            break
      
      self.__TELNET.send('wedge_power.sh reset -s\r')
      
      while True:
        if self.__TELNET.expect(['OpenBMC Release', 'minipack', 'Loading', 'i2c', 'gpio', 'g_cdc'], timeout= 180) == 0:
          break
          
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Reset the Minipack power and use scp funtion to copy PIM_MUX_check image to BMC, then verify the checksum of PIM CPLD in BMC.')
      server_file_path = self.image_server.local_check_image_path.replace(self.image_server.local_root_path, '') + '/' + self.__pim_mux_check_fileanme
      
      self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/' + self.__pim_mux_check_fileanme)
      
      for pim_id in range(1, self.__pim_count + 1):
        self.__TELNET.send('spimcpld_update.sh ' + str(pim_id) + ' /var/tmp/' + self.__pim_mux_check_fileanme + '\r')
        
        while True:
          if self.__TELNET.expect([self.__dut.ssh_credentials[5], '%'], timeout= 180) == 0:
            break
        
        result = re.search('(?i)' + new_pim_spi_mux_ver, self.__TELNET.getBuff(), re.M)
        
        if  result == None:
          self.__fail_count += 1
        
          UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': PIM' + str(j) + ' mux cpld is not match!!')
        else:
          UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': PIM' + str(j) + ' mux cpld is match!!')
          
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0350 Upgrade_MUXCPLD_for_PIM is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0350 Upgrade_MUXCPLD_for_PIM is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
