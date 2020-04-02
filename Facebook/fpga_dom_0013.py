#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0013(Script):
  """
  Class Name: FPGA_DOM_0013
  Purpose: Check FPGA reset function.
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check FPGA reset function.']

    purpose = [
      '1. Check FPGA reset function.']

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
    start_time = self.__SSH.minicycle_raw('0x40014', '', 'get')
    UI.log('1.	Read the uptime register on this PIM. Make sure the data is not zero.')
    
    print(int(start_time, 16))
    if int(start_time, 16) > 0:
        UI.log('PASS', 'The uptime is not zero.')
    else :
        UI.log('FAIL', 'The uptime is zero.')
    
    UI.log('2.	Write 0x1 to the reset register on this PIM and read the uptime register immediately.')
    self.__SSH.minicycle_raw('0x40020', '0x1', 'write')
    
    UI.log('3.	Check if the data from uptime register is zero.')
    end_time = self.__SSH.minicycle_raw('0x40014', '', 'get')
    
    print(int(end_time, 16))
    if int(end_time, 16) < 3:
        UI.log('PASS', 'The uptime is reset to zero.')
    else :
        UI.log('FAIL', 'The uptime is not reset to zero.')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()