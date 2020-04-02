#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *

class FPGA_IOB_0006(Script):
  """
  Class Name: FPGA_IOB_0006
  Purpose: Check the thread control register
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Verify thread control register']

    purpose = [
      '1. Check the thread control register.']

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
    UI.log('Get Thread control register.')
    thread = '0x' + self.__SSH.minicycle_raw('0x0024', '', 'get')
    # print(thread)
    if thread == '0x00000000':
        UI.log('S1. Write Thread control register with as ' + rand_value)
        self.__SSH.minicycle_raw('0x0024', rand_value, 'write')
        UI.log('S2. Check if Thread control register with is ' + rand_value)
        self.__SSH.minicycle_raw('0x0024', rand_value, 'read')

    else:
        UI.log('S1. Write Thread control register with as ' + rand_value)
        self.__SSH.minicycle_raw('0x0024', rand_value, 'write')
        UI.log('S2. The Thread control register should be ' + thread)
        self.__SSH.minicycle_raw('0x0024', thread, 'read')
        UI.log('S3. Write Thread control register with as ' + thread)
        self.__SSH.minicycle_raw('0x0024', thread, 'write')
        UI.log('S4. Check if Thread control register is 0x00000000')
        self.__SSH.minicycle_raw('0x0024', '0x00000000', 'read')
        UI.log('S5. Write Thread control register with as ' + rand_value)
        self.__SSH.minicycle_raw('0x0024', rand_value, 'write')
        UI.log('S6. Check if Thread control register with is ' + rand_value)
        self.__SSH.minicycle_raw('0x0024', rand_value, 'read')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()