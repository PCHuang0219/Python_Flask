#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0500(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Read DOM FPGA flash']
    purpose = ['To verify if the FPGA of DOM Module can be read via spi.']
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

    # ==================================================================================================
    UI.log('STEP#01', 'Set an IP for BMC eth0.')
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Erase IOB FPGA via spi and power reset.')
      self.__TELNET.send('fpga_ver.sh | grep DOMFPGA\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5], timeout= 20)
      
      for pim_id in range(1, self.__pim_count + 1):
        self.__TELNET.send('spi_util.sh erase spi2 PIM' + str(pim_id) + ' DOM_FPGA_FLASH\r')
        
        while True:
          if self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Done.', 'OK', ' '], timeout= 180) == 0:
            break
        
      time.sleep(3)
      self.__TELNET.send('wedge_power.sh reset -s\r')
      time.sleep(5)
      while True:
        x = self.__TELNET.expect(['OpenBMC Release', 'minipack', 'Loading', 'i2c', 'gpio', 'g_cdc', self.__dut.ssh_credentials[5]], timeout= 180)
        if x == 0:
          break
      
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('fpga_ver.sh | grep DOMFPGA\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5], timeout=20)
      
      for pim_id in range(1, self.__pim_count + 1):
        result = re.search('(?i)DOMFPGA is not detected or PIM ' + str(pim_id) + ' is not inserted', self.__TELNET.getBuff(), re.M)
        
        if  result == None:
          self.__fail_count += 1
        
          UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': PIM ' + str(pim_id) + ' did not erased.')
        else:
          UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': PIM ' + str(pim_id) + ' has been erased')
          
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0500 Erase_DOM_FPGA_flash is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0500 Erase_DOM_FPGA_flash is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
