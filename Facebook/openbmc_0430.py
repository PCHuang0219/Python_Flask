#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0430(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Power OFF/ON  Microserver']
    purpose = ['To verify the microserver is working properly when after power off and power on the Microserver.',
      'Run the "wedge_power.sh off" and "wedge_power.sh on" script to power off and power on the Microserver,',
      'Run the above steps for 100 iterations and check if the microserver comes back up each time and OS(ONIE or CentOS) boots correctly to the login prompt.']

    self.__dut = dut[1]
    self.image_server = image_server
    super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__TELNET = super().initUI(self.__dut.telnet_credentials, self.__dut.platform, OpenBMC)
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform, OpenBMC)
    self.__cycle = 1
    self.__fail_count = 0
    self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    self.__TELNET.send('sv stop mTerm\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Repeat ' + str(self.__cycle) + ' times with the command "wedge_power.sh off" and "wedge_power.sh on" to power off and power on the Microserver.')
      self.__TELNET.send('sol.sh\r')
      
      # SSH connection send and expect
      self.__SSH.send('wedge_power.sh off\r')
      self.__SSH.expect(self.__dut.ssh_credentials[5])
      self.__SSH.send('wedge_power.sh on\r')
      self.__SSH.expect(self.__dut.ssh_credentials[5])
      
      while True:
        try:
          x = self.__TELNET.expect(['~]# ', 'quit.', ']', 'IPv4.', 'IPv6.'], timeout=180)
          if x == 0:
            break
        except:
          self.__fail_count += 1
          break
          
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'To check if the microserver comes back up each time correctly.')
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
        
      if  self.__fail_count  == 0:
        self.__TELNET.send('log-util all --clear\r')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
      else:
        self.__TELNET.send('cat /mnt/data/logfile\r')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
        self.__TELNET.send('hexdump /mnt/data/sel1.bin\r')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
        self.__TELNET.send('bic-util scm --get_post_code\r')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': Hangs Error.')
        
        break
    
    if  self.__fail_count  == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0430 Power_OFF_ON_Microserver is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0430 Power_OFF_ON_Microserver is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
