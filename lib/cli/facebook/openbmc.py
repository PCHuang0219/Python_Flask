#!/usr/bin/python3
####################################################################################################

import time
from lib.ui import UI
from lib import settings

class OpenBMC(UI):
  def __init__(self, ui_credentials, platform):
    super().__init__(ui_credentials, platform=platform)
	# Define your API below this line.
  def enterBMCFromCOMe(self):
    BMC_username = 'root'
    BMC_password = '0penBmc'
    BMC_prompt = '# '
    return_char = '\r'
    login_count = 0
    UI.log('ACTION', 'Enter OpenBMC session from Micro-server')
    self.send('screen /dev/ttyACM0 \r\n')
    while True:
      i = self.expect(['bmc-oob. login: ', '(?i)Password.*', BMC_prompt])
      if i == 2:
        UI.log('PASS', 'Enter OpenBMC session from Micro-server is pass.')
        break
      elif i == 0:
        self.send(BMC_username + return_char)
      elif i == 1:
        self.send(BMC_password + return_char)
        login_count += 1

      if login_count > 2:
        UI.log('FAIL', 'Can not enter OpenBMC session from Micro-server.')
        if not settings.glb.print_to_stdout:
          print('CRITICAL ALERT: Login failed. Permission denied for username/password: %s/%s'
          %(BMC_username, BMC_password))

          UI.log('CRITICAL ALERT', 'Login failed. Permission denied for username/password: %s/%s'
          %(BMC_username, BMC_password))
          break

  def exitBMCThroughCOMe(self):
    self.send('\001')
    self.send(':quit \r\n')
    try:
      self.expect('#')
      UI.log('PASS', 'Exit OpenBMC session from Micro-server is pass.')
    except:
      UI.log('FAIL', 'Exit OpenBMC session from Micro-server is failed.')

  def enterCOMeFromBMC(self):
    self.send('sol.sh \r\n')
    time.sleep(1)
    self.send('\r')
    try:
      self.expect('#')
      UI.log('PASS', 'Enter COMe session from BMC is pass.')
    except:
      UI.log('FAIL', 'Enter COMe session from BMC is failed.')

  def exitCOMeThroughBMC(self):
    self.send('\x0c')
    self.send('x \r\n')
    try:
      self.expect('#')
      UI.log('PASS', 'Exit COMe session from BMC session is pass.')
    except:
      UI.log('FAIL', 'Exit COMe session from BMC session is failed.')

  def getImageFilename(self, filepath):
    steam_reader = open(filepath, 'r')

    file_content_list = steam_reader.read().split('\n')

    steam_reader.close()

    return file_content_list[0]

  def getImageVersion(self, filepath):
    steam_reader = open(filepath, 'r')

    file_content_list = steam_reader.read().split('\n')

    steam_reader.close()

    if  len(file_content_list) >= 2:
      if file_content_list[1].find(';') > -1:
        return file_content_list[1].split(';')
      else:
        return file_content_list[1]
    else:
      return file_content_list[0]