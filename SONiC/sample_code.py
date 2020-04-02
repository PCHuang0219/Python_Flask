#!/usr/bin/python3
####################################################################################################
"""
Module Name: sample_code.py
Purpose    : Example for using TMS framework

Description:
  There is one necessary parameter :
            - dut            : the DUT object on which testing is performed.

History     :
    Anber Huang 02/12/2020,created.

Copyright(c) Accton Technology Corporation, 2019.
"""
from lib.ui import UI
from lib.script import Script
from lib.cli.sonic.sonic_api import SONiC_API

class SONiC_sample(Script):
  """
  Class Name: SONiC_sample
  Purpose: Python Test Automation Script Example
  """

  def __init__(self, dut, job_id=""):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Accton TMS framework sample.']

    purpose = ['1. Display SONiC automation testing.']

    self.__dut = dut
    super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__TELNET = super().initUI(self.__dut.ssh_credentials, self.__dut.platform, SONiC_API)
    
    prompt = self.__dut.telnet_credentials[5]
    url = 'http://210.63.221.19:8888/sonic-broadcom.bin'

    # Using API from ../lib/cli/sonic/SONiC_API to execute function
    self.__TELNET.changeImageVersion(url)

    # Using traditional method step by step to execute function.
    UI.log("ACTION", "Install SONiC image from " + url)
    self.__TELNET.send('sudo sonic_installer install -y ' + url + ' \r')
    while True:
      x = self.__TELNET.expect(['\r', prompt, 'Downloading image'])
      if x == 1 :
        # Upgrade finished.
        UI.log("PASS", "Install SONiC image success.")
        break

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()

    # Stop logging the script.
    super().endLog()