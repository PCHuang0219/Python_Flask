#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0780(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Get COM-e MAC from BMC']
    purpose = ['To verify if the COM-e MAC can be print.']
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
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Get COM-e MAC address from BMC.')
      self.__TELNET.send('wedge_us_mac.sh\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      self.__wedge_mac = re.search('(?i)wedge_us_mac.sh(.*)' + self.__dut.ssh_credentials[3], self.__TELNET.getBuff().replace('\n', ''), re.M)
      
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sol.sh\r')
      self.__TELNET.expect('quit.')
      self.__TELNET.send('\r')
      self.__TELNET.expect('~]# ')
      self.__TELNET.send('ifconfig eth0\r')
      self.__TELNET.expect('~]# ')
      
      result = re.search('(?i)' + str(self.__wedge_mac.group(1)).strip() , self.__TELNET.getBuff().replace('\n', ''), re.M)
      
      if result == None:
        self.__fail_count += 1
      
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get MAC and COM-E MAC is not match.')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get MAC and COM-E MAC is match.')
        
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0780 Get_COM-e_MAC_from_BMC is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0780 Get_COM-e_MAC_from_BMC is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
