#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0720(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Read COM-e BIOS and BIC version']
    purpose = ['To verify the COM-e BIOS and BIC version.']
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
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Display or clear logs by the command.')
      # Get device
      self.__TELNET.send('bic-util scm --get_dev_id\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # result = re.search('(?i)Device', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get device failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get device success.')
      
      # Get GPIO
      self.__TELNET.send('bic-util scm --get_gpio\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # result = re.search('(?i)rsvd', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get GPIO failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get GPIO success.')
      
      # Get GPIO config
      self.__TELNET.send('bic-util scm --get_gpio_config\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # result = re.search('(?i)Direction', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get GPIO config failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get GPIO config success.')
        
      # Get config
      self.__TELNET.send('bic-util scm --get_config\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # result = re.search('(?i)POST', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get config failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get config success.')
      
      # Get post code
      self.__TELNET.send('bic-util scm --get_post_code\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # result = re.search('(?i)util_get_post_buf', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get post code failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get post code success.')
        
      # Get SDR
      self.__TELNET.send('bic-util scm --get_sdr\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # result = re.search('(?i)type', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get SDR failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get SDR success.')
        
      # Read sensor
      self.__TELNET.send('bic-util scm --read_sensor\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)sensor', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get SDR failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Get SDR success.')
        
      # Read fruid
      self.__TELNET.send('bic-util scm --read_fruid\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # result = re.search('(?i)MAC address', self.__TELNET.getBuff(), re.M)
      
      # if result == None:
        # self.__fail_count += 1
        
        # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Read fruid failure.')
      # else:
        # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Read fruid success.')
        
    # if self.__fail_count == 0:
      # UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0720 Get_information_of_bridge_ic is passed.')
    # else:
      # UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0720 Get_information_of_bridge_ic is failed.')
      
    UI.log('CHECK', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0720 Get_information_of_bridge_ic need to check.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
