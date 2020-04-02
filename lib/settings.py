#!/usr/bin/python3
######################################################################################################################################################
"""
Module Name: settings.py
Purpose: Settings and DUT configuration object definitions.

Description:
  This module is part of the lib package for the Python test automation framework containing class definitions for settings and configuration objects.

Copyright(c) Accton Technology Corporation, 2019
"""

import os
import sys

def init():
  global glb, host_os

  glb = GlobalUI_settings()

  # Check operating  system.
  if 'linux' in sys.platform:
    host_os = 'linux'
  elif 'win32' in sys.platform:
    host_os = 'windows'
  else:
    host_os = 'unknown: '+sys.platform

class GlobalUI_settings():
  """
  Class Name: GlobalUI_settings
  Purpose: Stores and configures global user interface settings.

  Public Attributes:
    ctrl_c - string constant for the CTRL+C character
    log_width - width of the displayed log; default is 100 characters.
    change_line - change line character string of the displayed log
    print_to_stdout - whether to print the log in the command prompt
    show_login - whether to show the login terminal output

  Public Methods:
    setVerbosity() - sets the verbosity level for display and log output.

  History: 2019/06/06 - Michael Chen, created.
  """

  def __init__(self, verbosity='medium'):
    """
    Constructor for GlobalUI_settings
    Input:
      verbosity - the initial verbosity level; default is 'medium'.
    """

    self.ctrl_c = '\x03'
    self.log_width = 100
    self.change_line = '\n\n'
    self.setVerbosity(verbosity)

  def setVerbosity(self, level):
    """
    Function Name: setVerbosity
    Purpose: Configures the login and display output verbosity
    Description: Toggles print_to_stdout and show_login between True and False.
    Input: level - 'high', 'medium' or 'low
    example: setVerbosity('low')
    """

    if level == 'high':
      self.print_to_stdout = True
      self.show_login = True
    elif level == 'medium':
      self.print_to_stdout = False
      self.show_login = True
    elif level == 'low':
      self.print_to_stdout = False
      self.show_login = False
   
class Minipack_COMe():
  def __init__(self):
    self.model_name = 'Minipack_COMe'
    self.platform = 'Facebook'
    self.console_credentials = ('console','',115200,'root','1111','~]# ')
    self.telnet_credentials = ('telnet','10.100.43.149','5001','root','1111','~]# ')
    self.ssh_credentials = ('ssh','10.100.43.132','22','root','1111','~]# ',)
    self.ssh_netmask = '255.255.252.0'
class Minipack_BMC():
  def __init__(self):
    self.model_name = 'Minipack_BMC'
    self.platform = 'Facebook'
    self.console_credentials = ('console','',115200,'root','0penBmc','~#')
    self.telnet_credentials = ('telnet','10.100.43.149','5001','root','0penBmc','~#')
    self.ssh_credentials = ('ssh','10.100.43.131','22','root','0penBmc','~#',)
    self.ssh_netmask = '255.255.252.0'
class AS7712_32X():
  def __init__(self):
    self.model_name = 'AS7712_32X'
    self.platform = 'SONiC'
    self.console_credentials = ('console','',115200,'admin','YourPaSsWoRd','$')
    self.telnet_credentials = ('telnet','192.168.40.10','5019','admin','YourPaSsWoRd','$')
    self.ssh_credentials = ('ssh','192.168.3.50','22','admin','YourPaSsWoRd','$',)
    self.ssh_netmask = '255.255.255.0'
class ATEN_PDU():
  def __init__(self):
    self.model_name = 'ATEN_PDU'
    self.platform = 'Facebook'
    self.console_credentials = ('console','',115200,'teladmin','password','> ')
    self.telnet_credentials = ('telnet','10.100.43.150','23','teladmin','password','> ')
    self.ssh_credentials = ('ssh','10.100.43.150','22','teladmin','password','> ',)
    self.ssh_netmask = '255.255.252.0'
class AS7816_64X():
  def __init__(self):
    self.model_name = 'AS7816_64X'
    self.platform = 'SONiC'
    self.console_credentials = ('console','',115200,'admin','YourPaSsWoRd',': ~$')
    self.telnet_credentials = ('telnet','192.168.40.50','5018','admin','YourPaSsWoRd',': ~$')
    self.ssh_credentials = ('ssh','192.168.40.64','22','admin','YourPaSsWoRd',': ~$',)
    self.ssh_netmask = '255.255.255.0'
