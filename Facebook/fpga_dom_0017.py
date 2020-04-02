#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0017(Script):
  """
  Class Name: FPGA_DOM_0017
  Purpose: QSFP interrupt and interrupt mask.
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['QSFP interrupt and interrupt mask.']

    purpose = [
      '1. QSFP interrupt and interrupt mask.']

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
    test_port = [14,15]
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('S1 Set Interrupt mask to be enabled.')
    self.__SSH.minicycle_raw('0x40068', '0xffffffff', 'write')
    
    UI.log('S2 Check the default interrupt is disabled.')
    self.__SSH.minicycle_raw('0x40060', '0x00000000', 'read')
    
    UI.log('S3 Trap QSFP modules to reset mode and check the registers. A QSFP module in reset mode will not causes the corresponding interrupt bit to be triggered.')
    self.__SSH.minicycle_raw('0x40070', '0xffffffff', 'write')
    self.__SSH.minicycle_raw('0x40060', '0x00000000', 'read')
    
    UI.log('S4 Reset interrupt status to default.')
    self.__SSH.minicycle_raw('0x40070', '0xffff0000', 'write')
    self.__SSH.minicycle_raw('0x40060', '0x00000000', 'read')
    
    UI.log('S5 Set Interrupt mask to be disabled.')
    self.__SSH.minicycle_raw('0x40068', '0x0', 'write')
        
    UI.log('S6 Trap QSFP modules to reset mode and check the registers. A QSFP module in reset mode will causes the corresponding interrupt bit to be triggered.')
    self.__SSH.minicycle_raw('0x40070', '0xffffffff', 'write')
    
    intterup_port = self.__SSH.minicycle_raw('0x40060', '', 'get')[4:8]
    if hex(int(gen_bin_byport(test_port),2))[2:6].upper() == intterup_port.upper():
        UI.log('PASS', 'The interrupt port is correct.')
    else :
        UI.log('FAIL', 'The interrupt port is incorrect.')
    # self.__SSH.minicycle_raw('0x40060', '0x00006000', 'read')
    
    
    UI.log('S7 Reset interrupt status to default.')
    self.__SSH.minicycle_raw('0x40070', '0xffff0000', 'write')
    self.__SSH.minicycle_raw('0x40060', '0x00000000', 'read')
    # self.__SSH.minicycle_raw('0x40070', '0xffffffff', 'read')

    # self.__SSH.minicycle_raw('0x40070', '0x0', 'write')
    # reset_port = self.__SSH.minicycle_raw('0x40070', '', 'get')[4:8]
    # UI.log('The reset port is ' + reset_port)

    # if hex(int(gen_bin_byport(test_port,reverse='true'),2))[2:6].upper() == reset_port.upper():
        # UI.log('PASS', 'The port in reset mode is correct.')
    # else :
        # UI.log('FAIL', 'The port in reset mode is incorrect.')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()