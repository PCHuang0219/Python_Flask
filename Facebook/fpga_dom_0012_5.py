#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0012_5(Script):
  """
  Class Name: FPGA_DOM_0012_5
  Purpose: Power interrupt
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check interrupt status.']

    purpose = [
      '1. Power interrupt.']

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
    UI.log('S1 Reset the Power Interrupt Status.')

    self.__SSH.minicycle_raw('0x40098', '0xffffffff', 'write')
    time.sleep(5)
    thread = self.__SSH.minicycle_raw('0x4002C', '', 'get')
    result = hex_2_32bin(thread)[25:26]
    print(result)
    if result == '0':
        UI.log('PASS', 'Power Interrupt status is 0.')
        
    else:
        UI.log('FAIL', 'Power Interrupt status is not 0.')
        
    UI.log('S2 Write 0x0 to enable Device Power Good Mask (0x40094).')
    self.__SSH.minicycle_raw('0x40094', '0x0', 'write')

    UI.log('S3 Write 0x0 to Device Power Control register (0x40098).')
    self.__SSH.minicycle_raw('0x40098', '0x0', 'write')
    
    UI.log('S4 Check the power interrupt status of Interrupt INTA Summary/MSI Interrupt Status.(0x4002C)')
    thread = self.__SSH.minicycle_raw('0x4002C', '', 'get')
    result = hex_2_32bin(thread)[25:26]
    print(result)
    if result == '1':
        UI.log('PASS', 'Power Interrupt register is 1.')
    else:
        UI.log('FAIL', 'Power Interrupt status is not 1')
        
    UI.log('S5 Reset the Power Interrupt Status.')

    self.__SSH.minicycle_raw('0x40098', '0xffffffff', 'write')
    time.sleep(5)
    thread = self.__SSH.minicycle_raw('0x4002C', '', 'get')
    result = hex_2_32bin(thread)[25:26]
    print(result)
    if result == '0':
        UI.log('PASS', 'Power Interrupt status is 0.')
        
    else:
        UI.log('FAIL', 'Power Interrupt status is not 0.')    
        
    UI.log('S6 Write 0xffffffff to disable Device Power Good Mask (0x40094).')
    self.__SSH.minicycle_raw('0x40094', '0xffffffff', 'write')
    
    UI.log('S7 Write 0x0 to Device Power Control register (0x40098).')
    self.__SSH.minicycle_raw('0x40098', '0x0', 'write')
    
    UI.log('S8 Check the power interrupt status of Interrupt INTA Summary/MSI Interrupt Status.(0x4002C)')
    thread = self.__SSH.minicycle_raw('0x4002C', '', 'get')
    result = hex_2_32bin(thread)[25:26]
    print(result)
    if result == '0':
        UI.log('PASS', 'Power Interrupt register is 0.')
    else:
        UI.log('FAIL', 'Power Interrupt status is not 0')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()