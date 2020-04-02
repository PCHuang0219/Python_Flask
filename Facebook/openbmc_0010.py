#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0010(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Access BMC - From Microserver']

    purpose = [
        '1. To verify BMC can be accessed through Microserver via serial interface.',
			  '2. The following command can be used: screen /dev/ttyACM0']

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
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform,OpenBMC)

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    self.__SSH.enterBMCFromCOMe()

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()