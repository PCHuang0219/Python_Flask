#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0026(Script):
  """
  Class Name: FPGA_DOM_0026
  Purpose: Device reset control
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Device reset control.']

    purpose = [
      '1. Device reset control.']

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
    pim_card = "1"
    test_port = [1,2]
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('S1 Reset the MDIO Interrupt Status.')
    self.__SSH.minicycle_raw('0x40084', '0x0', 'write')
    self.__SSH.minicycle_raw('0x4009c', '0x0', 'write')
    print('Wait for 120 seconds.')
    time.sleep(120)
    
    
    UI.log('S2 Write 0x0 to this register to trap PHYs in the reset mode.')
    self.__SSH.minicycle_raw('0x4009c', '0xFFFF0000', 'write')
    self.__SSH.minicycle_raw('0x40084', '0xf', 'write')

    print('Wait for 120 seconds.')
    time.sleep(120)
    
    # UI.log('S3 Invoke minicycle.py to get PHY ID.')
    # self.__SSH.minicycle_mdio(pim=pim_card, way='read', check_value='Fail to get PHY ID')
    # time.sleep(5)
    
    UI.log('S3 Write 0xFFFFFFFF to release PHYs from reset mode.')
    self.__SSH.minicycle_raw('0x4009C', '0xFFFFFFFF', 'write')
    print('Wait for 120 seconds.')
    time.sleep(120)
    
    UI.log('S4 Invoke minicycle.py to perform the test. The utility performs PHY direct access (reading Device ID 0x1358 and 0x1141) \
    and PHY indirect access (reading chip ID 0x1724, 0x0008, and chip revision information 0x00A1) to retrieve register data. \
    PHY direct access includes only reading data from PHY registers. PHY indirect access includes reading and writing transactions to PHY registers.')
    self.__SSH.minicycle_mdio(pim=pim_card, way='read', check_value='0x1358' )
    self.__SSH.minicycle_mdio(pim=pim_card, way='read', check_value='0x1141' )
    self.__SSH.minicycle_mdio(pim=pim_card, way='read', check_value='0x1724' )
    self.__SSH.minicycle_mdio(pim=pim_card, way='read', check_value='0x0008' )
    self.__SSH.minicycle_mdio(pim=pim_card, way='read', check_value='0x00A1' )
    time.sleep(5)
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()