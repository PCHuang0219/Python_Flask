#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *

class FPGA_DOM_0001(Script):
  """
  Class Name: FPGA_DOM_0001
  Purpose: Check the write data buffer in I2C RTC data block
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check the write data buffer in I2C RTC data block']

    purpose = [
      '1. Check the write data buffer in I2C RTC data block.']

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
    UI.log('Facebook DOM 0001')
    UI.log('S1 Check the write data buffer in I2C RTC data block. Coverage: PIM #1, RTC #0~#3, Descriptor #0~#3')
    thread = self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x0', desc='0')
    UI.log('S2 Generate a word-long random number.')
    random_hex = ByteToHexwith0x(rand_value)
    
    
    random_value = ByteToHex(rand_value)
    
    UI.log('S3 Write this random number to the write data buffer of RTC #0, descriptor #0 at offset 0x0.')
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x0', desc='0', check_value=random_hex)
    
    UI.log('S4 Check this random number is in the data buffer of RTC #0, descriptor #0 at offset 0x0.')
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x0', desc='0', check_value=random_value)
    
    UI.log('S5 Change the target offset to next word-long registers, repeat step 1 ~ step 3 till all the registers in the write data buffer of this descriptor are tested.')
    rand_value2 = generate_rand_hex()
    random_hex2 = ByteToHexwith0x(rand_value2)
    random_value2 = ByteToHex(rand_value2)
    
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x04', desc='0', check_value=random_hex2)
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x04', desc='0', check_value=random_value2)
    
    UI.log('S6 Repeat step 1 ~ step 4 till all the write data buffers of descriptor #0 ~ #3 of this RTC are tested.')
    rand_value3 = generate_rand_hex()
    random_hex3 = ByteToHexwith0x(rand_value3)
    random_value3 = ByteToHex(rand_value3)
    
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x0', desc='1', check_value=random_hex3)
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x0', desc='1', check_value=random_value3)
    
    rand_value4 = generate_rand_hex()
    random_hex4 = ByteToHexwith0x(rand_value4)
    random_value4 = ByteToHex(rand_value4)
    
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x0', desc='2', check_value=random_hex4)
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x0', desc='2', check_value=random_value4)
    
    rand_value5 = generate_rand_hex()
    random_hex5 = ByteToHexwith0x(rand_value5)
    random_value5 = ByteToHex(rand_value5)
    
    self.__SSH.minicycle_rtc(pim='1', way='write', port=test_port, offset='0x0', desc='3', check_value=random_hex5)
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port, offset='0x0', desc='3', check_value=random_value5)

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()