#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.cli.facebook.fpga import FPGA

class FPGA_IOB_0002(Script):
  """
  Class Name: FPGA_IOB_0002
  Purpose: Python Test Automation Script Example 1
  """

  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Python Example Script 1']

    purpose = [
      '1. Demonstrate how to initialize console, Telnet, and SSH UIs on the DUT.',
      '2. Demonstrate how to use CLI library to check DUT model name.',
      '3. If you have a string of characters that exceeds the maximum width of the source code '\
          'document width, this is how you should split the long string, including two indents on '\
          'each subsequent line.']

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

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    self.__SSH.minicycle_raw('0x0000', '0xA2041902', 'read')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()