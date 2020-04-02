#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0770(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Downgrade DOM FPGA']
    purpose = ['To verify if the FPGA of DOM Module can be write via spi.']
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
    self.__pim_16q_iob_fpga_ver = '16Q DOMFPGA: 1.0'
    self.__pim_16q_iob_fpga_filename = 'PIM_16Q_fpga_V1.0_20180627_1500.bit'
    self.__pim_type_list = {1:'16q', 2:'16q', 3:'16q', 4:'16q', 5:'16q', 6:'16q', 7:'16q', 8:'16q'}

    # ==================================================================================================
    UI.log('STEP#01', 'Set an IP for BMC eth0.')
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Check the version of IOB FPGA in BMC.')
      self.__TELNET.send('fpga_ver.sh | grep 16Q\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy IOB_downgrade_FPGA file to minipack then check the image is transfer correctlly.')
      server_file_path = self.image_server.local_old_image_path.replace(os.getcwd().replace('\\', '/'), '') + '/' + self.__pim_16q_iob_fpga_filename
      
      UI.log('DOM FPGA version is ' + os.path.splitext(self.__pim_16q_iob_fpga_ver)[0] + '.')
      
      self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
        server_file_path, '/var/tmp/minipack_pim_16q_old_fpga.bit')
        
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Write DOM_downgrade_FPGA via spi.')
      for pim_id in self.__pim_type_list:
        if self.__pim_type_list[pim_id] == '16q':
          self.__TELNET.send('spi_util.sh write spi2 PIM' + str(pim_id) + ' DOM_FPGA_FLASH /var/tmp/minipack_pim_16q_old_fpga.bit\r')
      
          while True:
            if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Done.', 'OK.', 'done.', 'VERIFIED'], timeout= 180) == 0:
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
      self.__TELNET.send('fpga_ver.sh | grep 16Q\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)' + self.__pim_16q_iob_fpga_ver, self.__TELNET.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': IOB FPGA version is NOT match!!')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': IOB FPGA version is match!!')
        
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0770 Downgrade_DOM_FPGA_flash is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0770 Downgrade_DOM_FPGA_flash is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
