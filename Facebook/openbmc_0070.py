#!/usr/bin/python3
####################################################################################################

import re
import random
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0070(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Monitoring All Sensors']
    purpose = [
      'To verify all sensors  can be accessed.', 
      '   Using the "sensors-util" command on openBMC to get the current view for all sensors.', 
      '   (ltc4151-i2c-7-6f is PS21 sensors, only for PSU21, need to insert the DC PSU into PS2)']

    self.__dut = dut[1]
    self.prompt = self.__dut.ssh_credentials[5]
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and TELNET UI with SystemMgmt APIs.
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform, OpenBMC)
    self.__fail_count = 0

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    self.__SSH.send('sensor-util all \r')
    self.__SSH.expect(self.prompt, timeout= 180)
    
    if self.__fail_count == 0:
      UI.log('PASS', 'BMC_0070 Monitoring All Sensors is passed.')
    else:
      UI.log('FAIL', 'BMC_0070 Monitoring All Sensors is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()