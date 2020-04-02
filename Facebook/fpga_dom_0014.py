#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.ui import UI
from lib.cli.facebook.fpga import FPGA
from lib.cli.facebook.fpga import *
import time

class FPGA_DOM_0014(Script):
  """
  Class Name: FPGA_DOM_0014
  Purpose: Check max. temperature register.
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Check max. temperature register.']

    purpose = [
      '1. Check max. temperature register.']

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
    test_port = "16"
    
    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('1.	Make sure that there is at least one optics QSFP module in one of the 16 ports on PIM #1.')
    
    UI.log('2.	Enable DOM auto-collection activity on this PIM.')
    self.__SSH.minicycle_raw('0x40410', '0x01000001', 'write')
    
    UI.log('3.	Do one time RTC collection.')
    self.__SSH.minicycle_rtc(pim='1', way='read', port=test_port)
    
    UI.log('4.	Check the data read from this register. Make sure that the data varies as time goes by.')
    start_temp = self.__SSH.minicycle_raw('0x40044', '', 'get')
    print('Wait 60 seconds.')
    time.sleep(60)
    
    end_temp = self.__SSH.minicycle_raw('0x40044', '', 'get')
    if start_temp == end_temp:
        UI.log('FAIL', 'The Max temperature is not changed.')
    else :
        UI.log('PASS', 'The Max temperature is changed.')
    
    max_temp = int(hex_2_dec(end_temp[4:8])) * 0.00390625
    print(max_temp)
    if max_temp != 0:
        UI.log('PASS', 'The Max temperature is ' + str(max_temp))
    else :
        UI.log('FAIL', 'The Max temperature is 0.')
        
    max_temp_location = int(hex_2_dec(end_temp[2:4])) + 1
    print(max_temp_location)
    if max_temp != 0:
        UI.log('PASS', 'The Max temperature is located at ' + str(max_temp_location))
    else :
        UI.log('FAIL', 'The Max temperature is not found.')
    
    UI.log('5.	Reset FPGA to default.')
    self.__SSH.minicycle_raw('0x40020', '0x1', 'write')
    time.sleep(60)
    
    end_temp = self.__SSH.minicycle_raw('0x40044', '', 'get')
    print(end_temp)
    if "00000000" == end_temp:
        UI.log('PASS', 'The Max temperature is reset to default.')
    else :
        UI.log('FAIL', 'The Max temperature is not reset.')
    
  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()