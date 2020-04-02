#!/usr/bin/python3
####################################################################################################

import re
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0050(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['To control GPIOs']
    purpose = ['By default, all GPIOs are configured as GPIOS as input. All minipack GPIOs can be found in "/tmp/gpionames".',
      'To use any GPIO, go into such GPIO directory and change the "direction" and "value" files.',
      'GPIOs can be control by changing the "direction" and "value" files in such GPIO directory.']
    
    self.__dut = dut[1]
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform,OpenBMC)
    self.__cycle = 1
    self.__value = ['0', '1']
    self.__direction = ['in', 'out']
    self.__fail_count = 0

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Select a GPIO to change the direction and value files.')
      self.__SSH.send('cd /tmp/gpionames\r')
      self.__SSH.expect('#')
      self.__SSH.send('ls -al\r')
      self.__SSH.expect('#')
      self.__SSH.send('cd BMC_FCM_B_MUX_SEL\r')
      self.__SSH.expect('#')
      
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Get direction and value responses.')
      self.__SSH.send('cat direction\r')
      self.__SSH.expect('#')
      
      direction = re.search('(?i)(in|out)+', self.__SSH.getBuff().replace('\n', ''), re.M)
      
      if direction.group(0) == 'in':
        self.__direction = ['out', 'in']
      else:
        self.__direction = ['in', 'out']
        
      self.__SSH.send('cat value\r')
      self.__SSH.expect('#')
      
      value = re.search('(?i)[0-1]+', self.__SSH.getBuff().replace('\n', ''), re.M)
      
      if value.group(0) == '0':
        self.__value = ['0', '1']
      else:
        self.__value = ['1', '0']
        
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Verify the direction can be configured.')
      
      self.__SSH.send('echo ' + self.__direction[0] + ' > direction\r')
      self.__SSH.expect('#')
      self.__SSH.send('cat direction\r')
      self.__SSH.expect('#')
      
      direction = re.search('(?i)(in|out)+', self.__SSH.getBuff().replace('\n', ''), re.M)
      
      if direction.group(0) == self.__direction[0]:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The direction is ' + direction.group(0) + '.')
      else:
        self.__fail_count += 1
      
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The direction is ' + direction.group(0) + ', shall be ' + self.__direction[0] + '.')
        
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Verify the value can be configured.')
      self.__SSH.send('echo ' + self.__value[0] + ' > value\r')
      self.__SSH.expect('#')
      self.__SSH.send('cat value\r')
      self.__SSH.expect('#')
      
      value = re.search('(?i)[0-1]+', self.__SSH.getBuff().replace('\n', ''), re.M)
      
      if value.group(0) == self.__value[0]:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The value is ' + value.group(0) + '.')
      else:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The value is ' + value.group(0) + ', shall be ' + self.__value[0] + '.')
        
      # ==================================================================================================
      UI.log('STEP#05 - cycle#' + str(i) + '/' + str(self.__cycle), 'set the value and direction as default.')
      self.__SSH.send('echo ' + self.__direction[1] + ' > direction\r')
      self.__SSH.expect('#')
      self.__SSH.send('echo ' + self.__value[1] + ' > value\r')
      self.__SSH.expect('#')
      
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0050 To_control_GPIOs is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0050 To_control_GPIOs is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()