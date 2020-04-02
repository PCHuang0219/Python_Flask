#!/usr/bin/python3
# This series of 150 #s defines the width for the content of this document; you should insert line breaks when your code exceeds this width. The tab
# size for this document is set to 2 spaces.
######################################################################################################################################################
# Use Docstring format to insert multiline comments.
"""Module Name: example_Script.py
Purpose: Python Test Automation Framework Example Script

Description:
  This example uses the serial port, Telnet, and SSH interface to display and check the DUT model.

Copyright(c) Accton Technology Corporation, 2019.
"""

from lib.script import Script

# Import the class containing your APIs from the associated module which you created.
from lib.cli.simba.system_mgmt import System_Mgmt

# Rename the class from "Example_Script" to your script name; Use Capitalized words and _ as separators for class names.
# Script classes shall inherit the base class Script located in lib.script.py.
class Example_Script(Script):
  """Class Name: Example_Script
  Purpose: Python Test Automation Example Script
  """

  def __init__(self, dut):
    """ Constructor for test scripts
    Attributes:
      dut - the DUT object on which testing is performed.
    """

    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Python Example Script 1']

    purpose = [
      '1. Demonstrate how to initialize console, Telnet, and SSH UIs on the DUT.',
      '2. Demonstrate how to use CLI library to check DUT model name.',
      '3. If you have a string of characters that exceeds the maximum width of the source code document width, this is how you should split the long'\
          'string, including two extra indents on  each subsequent new line.']

    self.__dut = dut
    super().__init__(headline, purpose, script_path=__file__)

  def run(self):
    """Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # Start logging the script.
    super().beginLog()

    # initialize serial, Telnet and SSH UI with System_Mgmt APIs.
    self.__CLI = super().initUI(self.__dut.console_credentials, self.__dut.platform, System_Mgmt)
    self.__TELNET = super().initUI(self.__dut.telnet_credentials, self.__dut.platform, System_Mgmt)
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform, System_Mgmt)

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    self.__CLI.chkSystemModel(model_name=self.__dut.model_name)
    self.__TELNET.chkSystemModel(model_name=self.__dut.model_name)
    self.__SSH.chkSystemModel(model_name=self.__dut.model_name)

  def stop(self):
    # Close interfaces and restore settings.
    self.__CLI.close()
    self.__TELNET.close()
    self.__SSH.close()

    # Stop logging the script.
    super().endLog()
