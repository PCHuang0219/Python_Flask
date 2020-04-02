#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0022(Script):
  """
  Class Name: FPGA_DOM_0022
  Purpose: Device power bad status
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Device power bad status.']

    purpose = [
      '1. Device power bad status.']

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
    UI.log('S1 Check the default value of Device power bad status is 0x0.')
    self.__SSH.minicycle_raw('0x4008C', '0xf', 'write')
    self.__SSH.minicycle_raw('0x40098', '0xFFFFFFFF', 'write')
    self.__SSH.minicycle_raw('0x40090', '0x00000000', 'read')
    
    
    UI.log('S2 Write bit patterns to Device Power Control register (0x40098) and check this register.')
    self.__SSH.minicycle_raw('0x4008C', '0x0', 'write')
    
    self.__SSH.minicycle_raw('0x40098', '0x00000000', 'write')
    
    reset_port = self.__SSH.minicycle_raw('0x40090', '', 'get')
    UI.log('The bit of Power bad status is ' + reset_port)
    
    if reset_port == '0x00000000':
        UI.log('FAIL', 'The The bit of Power bad status is incorrect.')
    else :
        UI.log('PASS', 'The The bit of Power bad status is correct.')
        
    UI.log('S3 Reset to default.')
    self.__SSH.minicycle_raw('0x40098', '0xFFFFFFFF', 'write')
    self.__SSH.minicycle_raw('0x40090', '0x00000000', 'read')
    self.__SSH.minicycle_raw('0x4008C', '0x0', 'write')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()