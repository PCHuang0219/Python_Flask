#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0020(Script):
  """
  Class Name: FPGA_DOM_0020
  Purpose: PHY firmware load control and status
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['PHY firmware load control and status.']

    purpose = [
      '1. PHY firmware load control and status.']

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

    UI.log('S2 Write 0xFFF0 to Device Reset Control register (0x4009C) to trap PHYs in reset mode.')
    self.__SSH.minicycle_raw('0x4009C', '0xFFF0', 'write')
    
    UI.log('S3 Write 0xFFFF to Device Reset Control register (0x4009C) to release PHY reset.')
    self.__SSH.minicycle_raw('0x4009C', '0xFFFF', 'write')
    
    UI.log('S4 Check PHY FW Load Control/Status register (0x40084). Make sure the value is 0x0. (FW load is disabled. No FW has been loaded.)')
    self.__SSH.minicycle_raw('0x40084', '0x00000000', 'read')
    
    UI.log('S5 Write 0xF to PHY FW Load Control/Status register.')
    self.__SSH.minicycle_raw('0x40084', '0xF', 'write')
    
    print('Wait for 20 seconds.')
    time.sleep(20)
    
    UI.log('S6 Check PHY FW Load Control/Status register. Make sure the value is 0xFF. (FW load is enabled. FW has been loaded).')
    self.__SSH.minicycle_raw('0x40084', '0x000000FF', 'read')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()