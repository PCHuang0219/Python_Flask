#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *

class FPGA_DOM_0012_4(Script):
  """
  Class Name: FPGA_DOM_0012_4
  Purpose: Trigger these events to test this register: Device interrupt
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Verify thread control register.']

    purpose = [
      '1. Trigger these events to test this register: Device interrupt.']

    self.__dut = dut[0][0]
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
    UI.log('S1 Reset the Device Interrupt Status.')
    
    
    self.__SSH.minicycle_raw('0x40084', '0xffffffff', 'write')
    self.__SSH.minicycle_raw('0x40098', '0xffffffff', 'write')
    thread = self.__SSH.minicycle_raw('0x40088', '', 'get')
    result = hex_2_32bin(thread)[29:32]
    print(result)
    if result == '000':
        UI.log('PASS', 'Interrupt register is all 0.')
    else:
        UI.log('FAIL', 'Interrupt register is not all 0.')
        
    UI.log('S2 Write 0x0 to PHY FW Load Control/Status register (0x40084) to disable firmware load.')
    self.__SSH.minicycle_raw('0x40084', '0x0', 'write')
    
    UI.log('S3 Write 0 to bit[26] in Device Power Control register (0x40098) to disable 1.8V power.')
    self.__SSH.minicycle_raw('0x40098', '0xFBFFFFFF', 'write')
    
    UI.log('S4 Make sure bit[3:0] in Device Interrupt Status register (0x40088) are all 1.')
    thread = self.__SSH.minicycle_raw('0x40088', '', 'get')
    result = hex_2_32bin(thread)[28:32]
    print(result)
    if result == '1111':
        UI.log('PASS', 'Interrupt register is all 1.')
    else:
        UI.log('FAIL', 'Interrupt register is not all 1.')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()