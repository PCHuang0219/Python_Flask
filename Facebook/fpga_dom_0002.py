#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *

class FPGA_DOM_0002(Script):
  """
  Class Name: FPGA_DOM_0002
  Purpose: Check the correctness of the data written to QSFP EEPROM through I2C RTC
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check the correctness of the data written to QSFP EEPROM through I2C RTC']

    purpose = [
      '1. Check the correctness of the data written to QSFP EEPROM through I2C RTC.']

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
    test_port = "15"
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('Facebook DOM 0002')
    UI.log('S1 Generate 16 byte-long random numbers.')
    
    random_hex = ByteToHexwith0x(rand_value)  
    random_value = ByteToHex(rand_value)
    
    UI.log('S2 Write the generated 16 random numbers to QSFP EEPROM at offset 0x0 in Port #1 using descriptor #0.')
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x0', desc='0', check_value=random_hex)
    
    UI.log('S3 Read the 16-byte data back and check the correctness.')
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x0', desc='0', check_value=random_value)
    
    UI.log('S4 Generate 16 byte-long random numbers.')
    rand_value2 = generate_rand_hex()
    random_hex2 = ByteToHexwith0x(rand_value2)
    random_value2 = ByteToHex(rand_value2)
    
    UI.log('S5 Write the generated 16 random numbers to QSFP EEPROM at offset 0x80 in Port #1 using descriptor #1.')
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x80', desc='1', check_value=random_hex2)
    
    UI.log('S6 Read the 16-byte data back and check the correctness.')
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x80', desc='1', check_value=random_value2)
    
    UI.log('S7 Generate 16 byte-long random numbers.')
    rand_value3 = generate_rand_hex()
    random_hex3 = ByteToHexwith0x(rand_value3)
    random_value3 = ByteToHex(rand_value3)
    
    UI.log('S8 Write the generated 16 random numbers to QSFP EEPROM at offset 0x0 in Port #1 using descriptor #2.')
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x0', desc='2', check_value=random_hex3)
    
    UI.log('S9 Read the 16-byte data back and check the correctness.')
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x0', desc='2', check_value=random_value3)
    
    UI.log('S10 Generate 16 byte-long random numbers.')
    rand_value4 = generate_rand_hex()
    random_hex4 = ByteToHexwith0x(rand_value4)
    random_value4 = ByteToHex(rand_value4)
    
    UI.log('S11 Write the generated 16 random numbers to QSFP EEPROM at offset 0x80 in Port #1 using descriptor #3.')
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x80', desc='3', check_value=random_hex4)
    
    UI.log('S12 Read the 16-byte data back and check the correctness.')
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x80', desc='3', check_value=random_value4)

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()