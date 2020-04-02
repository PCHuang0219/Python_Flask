#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0023(Script):
  """
  Class Name: FPGA_DOM_0023
  Purpose: Device power good mask
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Device power good mask.']

    purpose = [
      '1. Device power good mask.']

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
    test_port = [1,2]
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('S1 Enable Device Interrupt Mask')
    self.__SSH.minicycle_raw('0x4008C', '0x0', 'write')
    
    UI.log('S2 Write bit patterns to this register and check the power interrupt bit in Device Interrupt Status register (0x4002C).')
    self.__SSH.minicycle_raw('0x40098', '0x0', 'write')
    
    reset_port = hex_2_32bin(self.__SSH.minicycle_raw('0x4002C', '', 'get'))[25:26]
    UI.log('The bit [5] of Interrupt INTA Summary/MSI Interrupt Status is ' + reset_port)
    
    if reset_port == '1':
        UI.log('PASS', 'The [5] of Interrupt INTA Summary/MSI Interrupt Status is correct.')
    else :
        UI.log('FAIL', 'The [5] of Interrupt INTA Summary/MSI Interrupt Status is incorrect.')
        
    UI.log('Reset to default.')
    self.__SSH.minicycle_raw('0x40098', '0xffff', 'write')
    self.__SSH.minicycle_raw('0x4008C', '0xffff', 'write')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()