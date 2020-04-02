#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0021(Script):
  """
  Class Name: FPGA_DOM_0021
  Purpose: Device interrupt status and mask
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Device interrupt status and mask.']

    purpose = [
      '1. Device interrupt status and mask.']

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
    UI.log('S1 Write 0x0 to PHY FW Load Control/Status register (0x40084) to disable FW load.')
    self.__SSH.minicycle_raw('0x40084', '0x0', 'write')

    UI.log('S2 Write 0 to bit[26] in Device Power Control register (0x40098) to disable 1.8V.')
    self.__SSH.minicycle_raw('0x40098', '0x0', 'write')
    
    UI.log('S3 Check Device Interrupt Status register (0x40088).')
    # self.__SSH.minicycle_raw('0x4009C', '0xFFFF', 'write')
    
    reset_port = hex_2_32bin(self.__SSH.minicycle_raw('0x40088', '', 'get'))[28:31]
    UI.log('The bit [3:0] is ' + reset_port)
    
    if reset_port == '111':
        UI.log('PASS', 'The [3:0] of PHY is correct.')
    else :
        UI.log('FAIL', 'The [3:0] of PHY is incorrect.')
        
    UI.log('S4 Reset to default')
    self.__SSH.minicycle_raw('0x40084', '0xffffffff', 'write')
    self.__SSH.minicycle_raw('0x40098', '0xffffffff', 'write')
    
    UI.log('S5 Check Device Interrupt Status register (0x40088).')
    print('Wait for 120 seconds.')
    time.sleep(120)
    
    
    reset_port = hex_2_32bin(self.__SSH.minicycle_raw('0x40088', '', 'get'))[28:31]
    UI.log('The bit [3:0] is ' + reset_port)
    
    if reset_port == '000':
        UI.log('PASS', 'The [3:0] of PHY is correct.')
    else :
        UI.log('FAIL', 'The [3:0] of PHY is incorrect.')
        
    UI.log('S6 Write 0xF to PHY FW Load Control/Status register (0x40084) to enable FW load.')
    self.__SSH.minicycle_raw('0x40084', '0xF', 'write')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()