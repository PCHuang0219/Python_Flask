#!/usr/bin/python3
####################################################################################################
"""
Module Name: diag_main.py
Purpose    : Execute all diag item from Minipack

Description:
  There are three necessary parameter :
            - diag_test_item : reference Config/FB_minipack.csv
            - diag_test_type : reference Config/FB_minipack.csv
            - dut            : the DUT object on which testing is performed.

History     :
    Anber Huang 10/02/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

from lib.script import Script
from lib.cli.facebook.diag import Diag

class Diag_Main(Script):
  """
  Class Name: Diag_Main
  Purpose: Python Test Automation Script Example 1
  """

  def __init__(self, dut, diag_test_item, diag_test_type, case, job_id=""):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Accton Minipack Diagnostic Testing.']

    purpose = [
      '1. Accton Minipack Diagnostic Testing.',
          ]

    self.__dut = dut[0]
    super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
    self.diag_test_item = diag_test_item
    self.diag_test_type = diag_test_type
    self.case = case
    # Start logging the script.
    file_name = 'diag_' + self.diag_test_item
    super().beginLog(file_name=file_name)

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform, Diag)

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    self.__SSH.runDiagTest(self.diag_test_item, self.diag_test_type, self.case)

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()

    # Stop logging the script.
    super().endLog()