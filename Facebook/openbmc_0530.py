#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0530(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Use i2cdetect to access i2c busses']
    purpose = ['To verify if the I2C can be detect by BMC.']
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
    self.__i2c_detect = {}
    self.__cycle = 1
    self.__fail_count = 0

    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01', 'To show the I2C can be detect by BMC.')
      self.__TELNET.send('i2cdetect -y 1\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      self.__i2c_detect[0] = '00:          -- -- -- -- -- -- -- -- -- -- -- -- --'
      self.__i2c_detect[1] = '10: -- -- UU -- -- -- -- -- -- -- -- -- -- -- -- --'
      self.__i2c_detect[2] = '20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'
      self.__i2c_detect[3] = '30: -- -- -- -- -- -- -- -- -- -- UU -- -- -- -- --'
      self.__i2c_detect[4] = '40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'
      self.__i2c_detect[5] = '50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'
      self.__i2c_detect[6] = '60: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --'
      self.__i2c_detect[7] = '70: -- -- -- -- -- -- -- --'
            
      for i in range(0, len(self.__i2c_detect)):
        if re.search('(?i)' + self.__i2c_detect[i], self.__TELNET.getBuff(), re.M) == None:
          self.__fail_count += 1
      
      if self.__fail_count > 0:
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Use i2c detect  value is incorrect.')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Use i2c detect  value is correct.')
    
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0530 Use_i2cdetect_to_access_i2c_busses is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0530 Use i2cdetect to access i2c busses is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
