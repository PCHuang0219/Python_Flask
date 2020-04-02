#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0020(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Quit BMC - From Microserver']

    purpose = [
        '1. To verify BMC session can be quit through Microserver via serial interface.',
        '   The following key combinations can be used:',
        '       ctrl-a; then ":", then "quit"',
        '       Please note if the screen session is within a minicom session, and ctrl-a is your hot key for minicom, use "ctr-a; ctrl-a" to send out "ctrl-a".']

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
    self.__SSH.exitBMCThroughCOMe()

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()