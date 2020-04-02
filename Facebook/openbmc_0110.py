#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0110(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Rebooting BMC']
    purpose = ['To verify reboot of BMC is working properly.',
      'Run the "reboot" command on BMC\'s console. This will reboot the BMC\'s RTOS, COM-e module should not be affected.',
      'Reboot Open BMC 100 times and check if it comes back up every single time.',
      'It should be able to reach the login prompt.']

    self.__dut = dut[1]
    self.image_server = image_server
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__TELNET = super().initUI(self.__dut.telnet_credentials, self.__dut.platform, OpenBMC)
    self.__cycle = 10
    self.__sleep_time = 15
    self.__fail_count = 0

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    # ==================================================================================================
    UI.log('STEP#01', 'Stop mTerm process then start a serial over LAN session.')
    self.__TELNET.send('sv stop mTerm\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    self.__TELNET.send('sol.sh\r')
    self.__TELNET.expect('quit')
    self.__TELNET.send('\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    # ==================================================================================================
    UI.log('STEP#02', 'cd to path "/usr/local/bin/" in diag.')
    self.__TELNET.send('cd /usr/local/bin/\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    # ==================================================================================================
    UI.log('STEP#03', 'Press "Ctrl+x" to exit diag then reboot the openBMC.')
    self.__TELNET.send('\x18')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Check the prompt is still "[root@minipack bin]#" in COM-e when openBMC boots completed.')
      self.__TELNET.send('reboot\r')
      
      
      while True:
        self.__TELNET.expect('OpenBMC Release')
        if 'login' in self.__TELNET.getBuff():
          break
          
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#05 - cycle#' + str(i) + '/' + str(self.__cycle), 'Repeat ' + str(i) + '/' + str(self.__cycle) + ' times to check the microserver should not be affected when the BMC is rebooting.')
      self.__TELNET.send('sol.sh\r')
      self.__TELNET.expect('quit')
      self.__TELNET.send('\r')
      
      try:
        self.__TELNET.expect(self.__dut.ssh_credentials[5], timeout=180)
        self.__TELNET.send('\x18')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
        self.__TELNET.send('log-util all --clear\r')
        time.sleep(10)
      except:
        self.__fail_count += 1
        break
    
    if self.__fail_count == 0:
      self.__TELNET.send('sol.sh\r')
      self.__TELNET.expect('quit')
      self.__TELNET.send('\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cd\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0110 Rebooting_BMC is passed.')
    else:
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cat /mnt/data/logfile\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('hexdump /mnt/data/sel1.bin\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('bic-util scm --get_post_code\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Hangs Error.')
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0110 Rebooting_BMC is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()