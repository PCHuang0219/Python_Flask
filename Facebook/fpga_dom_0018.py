#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0018(Script):
  """
  Class Name: FPGA_DOM_0018
  Purpose: QSFP port reset.
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['QSFP port reset.']

    purpose = [
      '1. QSFP port reset.']

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
    UI.log('S1 Trap QSFP modules to reset mode and check the register. ')
    self.__SSH.minicycle_raw('0x40070', '0xffffffff', 'write')
    self.__SSH.minicycle_raw('0x40070', '0xffffffff', 'read')

    self.__SSH.minicycle_raw('0x40070', '0x0', 'write')
    reset_port = self.__SSH.minicycle_raw('0x40070', '', 'get')[4:8]
    UI.log('The reset port is ' + reset_port)

    if hex(int(gen_bin_byport(test_port,reverse='true'),2))[2:6].upper() == reset_port.upper():
        UI.log('PASS', 'The port in reset mode is correct.')
    else :
        UI.log('FAIL', 'The port in reset mode is incorrect.')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()