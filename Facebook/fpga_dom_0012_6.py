#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0012_6(Script):
  """
  Class Name: FPGA_DOM_0012_6
  Purpose: MDIO interrupt: Get PHY IDs through MDIO bus.
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check interrupt status.']

    purpose = [
      '1. MDIO interrupt: Get PHY IDs through MDIO bus.']

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
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('S1 Reset the MDIO Interrupt Status.')
    self.__SSH.minicycle_raw('0x40084', '0x0', 'write')
    self.__SSH.minicycle_raw('0x4009c', '0x0', 'write')
    print('Wait for 120 seconds.')
    time.sleep(120)
    self.__SSH.minicycle_raw('0x4009c', '0xffff', 'write')
    self.__SSH.minicycle_raw('0x40084', '0xf', 'write')

    print('Wait for 120 seconds.')
    time.sleep(120)

    thread = self.__SSH.minicycle_raw('0x40084', '', 'get')
    result = hex_2_32bin(thread)[24:31]
    print(result)

    thread = self.__SSH.minicycle_raw('0x4002C', '', 'get')
    result = hex_2_32bin(thread)[24:25]
    print(result)
    if result == '0':
        UI.log('PASS', 'MDIO Interrupt register is 0.')
        
    else:
        UI.log('FAIL', 'MDIO Interrupt register is not 0.')
    

    self.__SSH.minicycle_raw('0x40214', '0x0', 'write')
    self.__SSH.minicycle_raw('0x40200', '0x00000014', 'write')
    
    UI.log('S2 Execute 1 time mdio query.')

    self.__SSH.minicycle_mdio(pim=pim_card, way='write')
    time.sleep(5)


    UI.log('S3 Check the MDIO interrupt status of Interrupt INTA Summary/MSI Interrupt Status.(0x4002C)')
    thread = self.__SSH.minicycle_raw('0x4002C', '', 'get')
    result = hex_2_32bin(thread)[24:25]
    print(result)
    if result == '1':
        UI.log('PASS', 'MDIO Interrupt register is 1.')
    else:
        UI.log('FAIL', 'MDIO Interrupt status is not 1')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()