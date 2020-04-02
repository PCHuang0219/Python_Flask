#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *

class FPGA_IOB_0003(Script):
  """
  Class Name: FPGA_IOB_0003
  Purpose: Check scratch pad register
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check scratch pad register']

    purpose = [
      '1. Read the raw data by tool mimicycle.']

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
    self.__SSH.minicycle_raw('0x0004', rand_value, 'write')
    self.__SSH.minicycle_raw('0x0004', rand_value, 'read')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()