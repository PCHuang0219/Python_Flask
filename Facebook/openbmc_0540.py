#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0540(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Use i2cget to access i2c busses']
    purpose = ['To verify if the I2C can be get by BMC.']
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

    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01', 'To show the I2C can be detect by BMC.')
      self.__TELNET.send('i2cget -y 10 0x6f\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)0x', self.__TELNET.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Can not to use the command getting the value of i2c bus.')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Can using the command to get the value of i2c bus.')
        
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0540 Use i2cget to access i2c busses is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0540 Use i2cget to access i2c bussesis failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
