#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0027(Script):
  """
  Class Name: FPGA_DOM_0027
  Purpose: Verify MDIO error status by holding PHY in reset status
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Verify MDIO error status by holding PHY in reset status.']

    purpose = [
      '1. Verify MDIO error status by holding PHY in reset status.']

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
    # UI.log('S1 Write 0x0 to PHY FW Load Control/Status register (0x40084) to disable FW load.')
    # self.__SSH.minicycle_raw('0x40084', '0x0', 'write')

    # UI.log('S2 Write 0xFFF0 to Device Reset Control register (0x4009C) to trap PHYs in reset mode.')
    # self.__SSH.minicycle_raw('0x4009C', '0xFFF0', 'write')
    # print('Wait for 120 seconds.')
    # time.sleep(120)
    
    UI.log('S1 Write 0xFFFFFFFE to Device Reset Control register (0x4009C) to trap the PHY #1 in the reset mode and make sure the bit[1] in MDIO Status register (0x40210) is 0.')
    self.__SSH.minicycle_raw('0x40210', '0x1', 'write')
    # self.__SSH.minicycle_raw('0x40084', '0x0', 'write')
    self.__SSH.minicycle_raw('0x4009c', '0xFFFFFFFE', 'write')
    
    print('Wait for 120 seconds.')
    time.sleep(120)
    
    reset_port = hex_2_32bin(self.__SSH.minicycle_raw('0x40210', '', 'get'))[31:32]
    UI.log('The bit 1 is ' + reset_port)
    
    if reset_port == '0':
        UI.log('PASS', 'The bit 1 in MDIO Status register (0x40210) is correct.')
    else :
        UI.log('FAIL', 'The bit 1 in MDIO Status register (0x40210) is incorrect.')
    
    # UI.log('S2 Write 0x0 to this register to trap PHYs in the reset mode.')
    # self.__SSH.minicycle_raw('0x4009c', '0xFFFF0000', 'write')
    # self.__SSH.minicycle_raw('0x40084', '0xf', 'write')

    # print('Wait for 120 seconds.')
    # time.sleep(120)
    
    UI.log('S2 Invoke minicycle.py separately to access PHY #1 through MDIO bus.')
    self.__SSH.minicycle_mdio(pim=pim_card, way='write', phy='1')
    time.sleep(5)
    
    UI.log('S3 Check the bit[1] in MDIO Status register (0x40210) after each PHY access. \
    Make sure bit[1] in MDIO Status register becomes 1 when accessing the PHY which is trapped in reset mode. Access to other PHYs does not trigger this bit.')
    reset_port = hex_2_32bin(self.__SSH.minicycle_raw('0x40210', '', 'get'))[31:32]
    UI.log('The bit 1 is ' + reset_port)
    
    if reset_port == '1':
        UI.log('PASS', 'The bit 1 in MDIO Status register (0x40210) is correct.')
    else :
        UI.log('FAIL', 'The bit 1 in MDIO Status register (0x40210) is incorrect.')
        
    UI.log('S4 Write 0xFFFFFFFD to Device Reset Control register (0x4009C) to trap the PHY #1 in the reset mode and make sure the bit[1] in MDIO Status register (0x40210) is 0.')
    self.__SSH.minicycle_raw('0x40210', '0x1', 'write')
    self.__SSH.minicycle_raw('0x4009c', '0xFFFFFFFD', 'write')
    
    print('Wait for 120 seconds.')
    time.sleep(120)
    
    reset_port = hex_2_32bin(self.__SSH.minicycle_raw('0x40210', '', 'get'))[31:32]
    UI.log('The bit 1 is ' + reset_port)
    
    if reset_port == '0':
        UI.log('PASS', 'The bit 1 in MDIO Status register (0x40210) is correct.')
    else :
        UI.log('FAIL', 'The bit 1 in MDIO Status register (0x40210) is incorrect.')
        
    UI.log('S5 Invoke minicycle.py separately to access PHY #2 through MDIO bus.')
    self.__SSH.minicycle_mdio(pim=pim_card, way='write', phy='2')
    time.sleep(5)
    
    UI.log('S6 Check the bit[1] in MDIO Status register, the MDIO status register is not changed.')
    reset_port = hex_2_32bin(self.__SSH.minicycle_raw('0x40210', '', 'get'))[31:32]
    UI.log('The bit 1 is ' + reset_port)
    
    if reset_port == '0':
        UI.log('PASS', 'The bit 1 in MDIO Status register (0x40210) is correct.')
    else :
        UI.log('FAIL', 'The bit 1 in MDIO Status register (0x40210) is incorrect.')
    
    # UI.log('S4 Write 0xFFFFFFFF to release PHYs from reset mode.')
    # self.__SSH.minicycle_raw('0x4009C', '0xFFFFFFFF', 'write')
    # print('Wait for 120 seconds.')
    # time.sleep(120)
    
    # UI.log('S5 Invoke minicycle.py to get PHY ID. Make sure all the transactions succeed.')
    # self.__SSH.minicycle_mdio(pim=pim_card, way='read', check_value='0x' )
    # time.sleep(5)
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()