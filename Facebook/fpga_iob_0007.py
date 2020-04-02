#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *

class FPGA_IOB_0007(Script):
  """
  Class Name: FPGA_IOB_0007
  Purpose: Check interrupt status
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check interrupt status']

    purpose = [
      '1. Check interrupt status.']

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
    rand_value = generate_rand_hex()
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('Facebook IOB 0007')
    UI.log('S1 Get the interrupt register.')
    thread = self.__SSH.minicycle_raw('0x002C', '', 'get')
    UI.log('S2 Generate interrupt to register 0x0044')
    self.__SSH.minicycle_raw('0x0044', '0x0', 'write')
    UI.log('S3 Get the interrupt register again.')
    thread = self.__SSH.minicycle_raw('0x002C', '', 'get')
    UI.log('S4 Check the bit 0 of register 0x002C.')
    result = hex_2_32bin(thread)[31:32]
    if result == '1':
        UI.log('PASS', 'Interrupt register is 1.')
    else:
        UI.log('FAIL', 'Interrupt register is 0.')
    self.__SSH.minicycle_raw('0x0044', '0xffff', 'write')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()