#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0100(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Power Cycling Microserver']
    purpose = [
      'To verify power cycling of microserver is working properly.',
      'Run the "wedge_power.sh reset" script to power cycle the Microserver.',
      'Run the above steps for 100 iterations and check if the microserver comes back up each time and OS(ONIE or CentOS) boots correctly to the login prompt.']

    self.__dut = dut[1]
    self.image_server = image_server
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()
    self.prompt = self.__dut.telnet_credentials[5]
  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__TELNET = super().initUI(self.__dut.telnet_credentials, self.__dut.platform, OpenBMC)
    self.__cycle = 10
    self.__fail_count = 0

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    UI.log('STEP#01', 'Stop mTerm process then start a serial over LAN session.')
    self.__TELNET.send('sv stop mTerm\r')
    self.__TELNET.expect(self.prompt)
    self.__TELNET.send('sol.sh\r')
    self.__TELNET.expect('quit')
    self.__TELNET.send('\r')
    self.__TELNET.expect(self.prompt)
    self.__TELNET.send('\x18')
    self.__TELNET.expect(self.prompt)
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Check the microserver can boot up success.')
      self.__TELNET.send('wedge_power.sh reset\r')
      self.__TELNET.expect(self.prompt)
      self.__TELNET.send('sol.sh\r')
      
      while True:
        try:
          if self.__TELNET.expect(['~]#', 'quit.', ']', 'IPv4.', 'IPv6.'], timeout=180) == 0:
            break
        except:
          self.__fail_count += 1
          break
        
      self.__TELNET.send('\r')
      self.__TELNET.expect(self.prompt)
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Press "Ctrl+x" to exit diag then reset the COM-e.')
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.prompt)
      
      if self.__fail_count == 0:
        # ==================================================================================================
        UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Repeat ' + str(i) + '/' + str(self.__cycle) + ' times to check the microserver can boot up successfully every times.')
        self.__TELNET.send('log-util all --clear\r')
        self.__TELNET.expect(self.prompt)
      else:
        self.__TELNET.send('cat /mnt/data/logfile\r')
        self.__TELNET.expect(self.prompt)
        self.__TELNET.send('hexdump /mnt/data/sel1.bin\r')
        self.__TELNET.expect(self.prompt)
        self.__TELNET.send('bic-util scm --get_post_code\r')
        self.__TELNET.expect(self.prompt)
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Hangs Error.')
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0100 Power_Cycling_Microserver is failed.')
      
        break
        
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0100 Power_Cycling_Microserver is passed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()