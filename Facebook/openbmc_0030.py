#!/usr/bin/python3
####################################################################################################

from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0030(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Quit BMC - From Microserver']

    purpose = [
        'To verify microserver can be accessed by using serial over LAN (SoL).',
        'The script to enable serial over LAN connections is located in "/usr/local/fbpackages/utils".',
        'Run "sol.sh" to start a serial over LAN session. Use the respective micro-server login credentials to gain access to the console. Press "Ctrl + X" to exit.']

    self.__dut = dut[1]
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
    self.__SSH.enterCOMeFromBMC()
    self.__SSH.exitBMCThroughCOMe()

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()