#!/usr/bin/python3
####################################################################################################

import re
import random
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0060(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Fan Control - Set Fan Speed']
    purpose = [
      'To verify the fan speed can be set manually.',
      'The speed coverage from 20% to 100% of full fan speed can be tested by increasing 10% each time. That is 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100% of full fan speed.',
      'All fan speeds behave as per spec tolerance of +/- 10% and not absolute values.',
      '',
      'To set the fan speed safely, first disable the fan controller by using the command "killall fand".', 
      'In order to start the fan controller after, just use the command "fand".', 
      'In addition, watchdog is bound with fand. After disabling fand, disable watchdog (watchdog_ctrl.sh off)',
      'immediately. Otherwise, watchdog will reset BMC in about 11 seconds.',
      'After killed fand, to manually set fan speed, use "set_fan_speed.sh <PERCENT (0..100)> <Fan Unit (1..8)>".']

    self.__dut = dut[1]
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and TELNET UI with SystemMgmt APIs.
    self.__TELNET = super().initUI(self.__dut.telnet_credentials, self.__dut.platform, OpenBMC)
    self.__bais = 10
    self.__cycle = 1
    self.__fan_count = 8
    self.__fail_count = 0

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'stop daemon and watchdog process.')
      self.__TELNET.send('sv stop fscd\r')
      self.__TELNET.expect('#')
      self.__TELNET.send('wdtcli stop\r')
      self.__TELNET.expect('#')
      
      for fan_index in range(1, self.__fan_count + 1):
      	speed = random.randint(1, 100)
      	
      	# ==================================================================================================
      	UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Set fan ' + str(fan_index) + ' speed.')
      	self.__TELNET.send('set_fan_speed.sh ' + str(speed) + ' ' + str(fan_index) + '\r')
      	self.__TELNET.expect('#')
      	
      	# ==================================================================================================
      	UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Get fan ' + str(fan_index) + ' speed.')
      	self.__TELNET.send('get_fan_speed.sh ' + str(fan_index) + '\r')
      	self.__TELNET.expect('#')
      	
      	get_speed = re.search('(?i)([0-9]+)%', self.__TELNET.getBuff(), re.M)
      	
      	# ==================================================================================================
      	UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'To verify fan ' + str(fan_index) + ' the percent of speed between set and get are match.')
      	if abs(speed - int(get_speed.group(1))) < self.__bais:
          UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The Verification of fan(' + get_speed.group(1) + ') is passed.')
      	else:
          self.__fail_count += 1
          
          UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The Verification of fan(' + get_speed.group(1) + ') is failed.')
          
    self.__TELNET.send('wedge_power.sh reset -s\r')
    
    while True:
      if self.__TELNET.expect(['OpenBMC Release', 'minipack', 'Loading', 'i2c', 'gpio', 'g_cdc', '\r', '\n'], timeout= 180) == 0:
        break

    expect_index = self.__TELNET.expect(['login:', '#'])
      
    if expect_index == 0:
      self.__TELNET.send('root\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send('0penBmc\r')
    
    self.__TELNET.expect('#')
    self.__TELNET.send('sv stop mTerm\r')
    self.__TELNET.expect('#')
    
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0060 Fan_Control_Set_Fan_Speed is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0060 Fan_Control_Set_Fan_Speed is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()