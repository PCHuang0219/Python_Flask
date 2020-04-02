#!/usr/bin/python3
######################################################################################################################################################
"""Module Name: script.py
Purpose: Definition for the Script class.

Description:
  The Script class handels tasks to be performed before and after the execution of each script. It also implements common methods for all scripts.

Copyright(c) Accton Technology Corporation, 2019.
"""

import os
import re
from datetime import datetime
from lib.ui import UI
import shutil

class Script():
  """Class Name: Script
  Purpose: Base class for scripts.
  """

  def __init__(self, headline='', purpose='', actions=[], script_path='', job_id=""):
    self.__name = str(self.__class__).strip('\'>').split('.')[-1]
    self.__headline = headline
    self.__purpose = purpose
    self.__actions = actions
    script_dir = os.path.dirname(os.path.abspath(script_path))
    script_dir = script_dir.replace('\\', '/')
    root = os.getcwd()
    root = root.replace('\\', '/')
    ### Need Michael fix : self.__log_path for windows
    self.__log_path = '../../report/' + job_id
    self.__start = -1
    self.__end = -1
    self.__duration = -1

  def initUI(self, ui_credentials, platform, *Libs):
    if 'host' in ui_credentials[0]:
      HOST = type('HOST', Libs, dict(HOST='HOST'))
      return HOST()
    elif 'snmp' in ui_credentials[0]:
      SNMP = type('SNMP', Libs, dict(SNMP='SNMP'))
      return SNMP(ui_credentials, platform)
    elif 'console' in ui_credentials[0]:
      CLI = type('CLI', Libs, dict(CLI='CLI'))
      return CLI(ui_credentials, platform)
    elif 'telnet' in ui_credentials[0]:
      TELNET = type('TELNET', Libs, dict(TELNET='TELNET'))
      return TELNET(ui_credentials, platform)
    elif 'ssh' in ui_credentials[0]:
      SSH = type('SSH', Libs, dict(SSH='SSH'))
      return SSH(ui_credentials, platform)

  def beginLog(self, file_name=''):
    if file_name == '':
      file_name = self.__name

    self.__log_name = file_name +'.log'

    if not os.path.exists(self.__log_path):
      os.makedirs(self.__log_path)

    UI.openLog(self.__log_path+'/'+self.__log_name)
    UI.logTitle('INITIALIZING SCRIPT '+self.__name)

    if self.__headline != '':
      UI.log('HEADLINE', *self.__headline)

    if self.__purpose != '':
      UI.log('PURPOSE', *self.__purpose)

    self.__start = datetime.now()
    UI.log('BEGIN LOG', 'Start time: '+str(self.__start).split('.')[0])

  def endLog(self):
    self.__end = datetime.now()
    self.__duration = self.__end-self.__start
    UI.log('END LOG', 'End time: '+str(self.__end).split('.')[0], 'Duration: '+str(self.__duration))
    UI.logTitle(UI.test_result)
    UI.closeLog()

    if os.path.exists(self.__log_path+'/PASS - '+self.__log_name):
      os.remove(self.__log_path+'/PASS - '+self.__log_name)

    if os.path.exists(self.__log_path+'/FAIL - '+self.__log_name):
      os.remove(self.__log_path+'/FAIL - '+self.__log_name)

    if os.path.exists(self.__log_path+'/CHECK - '+self.__log_name):
      os.remove(self.__log_path+'/CHECK - '+self.__log_name)

    if os.path.exists(self.__log_path+'/EXCEPTION - '+self.__log_name):
      os.remove(self.__log_path+'/EXCEPTION - '+self.__log_name)

    shutil.copyfile(self.__log_path+'/'+self.__log_name, self.__log_path+'/'+UI.test_result+' - '+self.__log_name)
    
  def getHeadline(self):
    return self.__headline

  def getPurpose(self):
    return self.__purpose
