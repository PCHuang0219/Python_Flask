#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0024(Script):
  """
  Class Name: FPGA_DOM_0024
  Purpose: Device power control
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Device power control.']

    purpose = [
      '1. Device power control.']

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
    UI.log('S1 Write bit patterns to this register and check the bit patterns in this register.')
    self.__SSH.minicycle_raw('0x4008C', '0x0', 'write')
    
    self.__SSH.minicycle_raw('0x40098', '0x00000000', 'write')
    self.__SSH.minicycle_raw('0x40098', '0x00000000', 'read')
    
    self.__SSH.minicycle_raw('0x40098', '0xFFFFFFFF', 'write')
    self.__SSH.minicycle_raw('0x40098', '0xFFFFFFFF', 'read')
    
        
    UI.log('S2 Reset to default.')
    self.__SSH.minicycle_raw('0x40098', '0xFFFFFFFF', 'write')
    self.__SSH.minicycle_raw('0x40090', '0x00000000', 'read')
    self.__SSH.minicycle_raw('0x4008C', '0x0', 'write')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()