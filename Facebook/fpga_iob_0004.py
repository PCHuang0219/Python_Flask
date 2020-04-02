#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_IOB_0004(Script):
  """
  Class Name: FPGA_IOB_0004
  Purpose: Check if the uptime is changed
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Verify uptime register']

    purpose = [
      '1. Check if the uptime is changed.']

    self.__dut = dut[0]
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform,FPGA)
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('Get the first uptime.')
    start_time = self.__SSH.minicycle_raw('0x0014', '', 'get')
    time.sleep(5)
    UI.log('Get the second uptime.')
    end_time = self.__SSH.minicycle_raw('0x00014', '', 'get')
    
    UI.log('Check if the uptime is increased.')
    result = int(end_time, 16) - int(start_time, 16)
    if result > 0:
        UI.log('PASS', 'The uptime is increased.')
    else :
        UI.log('FAIL', 'The uptime is not increased.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()