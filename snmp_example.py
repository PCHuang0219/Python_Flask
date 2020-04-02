#!/usr/bin/python3
######################################################################################################################################################
"""Module Name: snmp_example.py
Purpose: Example for using the SNMP UI.
Copyright(c) Accton Technology Corporation, 2019.
"""

from lib.script import Script
from lib.ui import UI

class SNMP_Example(Script):
  """Class Name: SNMP_Example
  Purpose: SNMP UI Example Script using snmpGet and snmpSet.
  """

  def __init__(self):
    headline = ['SNMP Example Script']
    purpose = ['Example for using the snmpGet and snmpSet methods.']
    self.snmp_credentials = ('snmp', '192.168.20.138', '2c')
    super().__init__(headline, purpose, script_path=__file__)

  def run(self):
    super().beginLog()
    SNMP = super().initUI(self.snmp_credentials, 'Simba', UI)
    setAndGetHostName(SNMP, oid='1.3.6.1.2.1.1.5.0', host_name='MyHostName')
    hello()

  def stop(self):
    super().endLog()

def setAndGetHostName(ui, oid, host_name):
  ui.snmpSet({oid: host_name})
  ui.snmpGet([oid])

s = SNMP_Example()

try:
  s.run()
  s.stop()
except Exception as e:
  UI.log('RAISE EXCEPTION', str(e))
  UI.test_result = 'EXCEPTION'
  s.stop()
