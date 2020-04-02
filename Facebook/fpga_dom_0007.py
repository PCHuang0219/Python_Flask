#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *

class FPGA_DOM_0007(Script):
  """
  Class Name: FPGA_DOM_0007
  Purpose: Check Device ID, FPGA revision, Board ID
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check Device ID, FPGA revision, Board ID']

    purpose = [
      '1. Check Device ID, FPGA revision, Board ID.']

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
    UI.log('Facebook DOM 0007')
    UI.log('S1 Read 1 word from this register on PIM #1.')
    UI.log('S2 According to the format of the bit pattern in this register, check if Device ID, FPGA revision, and Board ID in this register meet the system configuration.')
    self.__SSH.minicycle_raw('0x40000', '0xA3041200', 'read')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()