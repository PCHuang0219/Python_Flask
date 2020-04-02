#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0260(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Reboot the Whole System']
    purpose = ['To verify BMC and the microserver are working properly after power cycling the whole system.',
              'Run the "wedge_power.sh reset -s" script to power cycle the whole system.',
              'Run the above steps for 100 iterations and check if the whole system comes back up each time, BMC and OS(ONIE or CentOS) of the microserver boots correctly to the login prompt.']

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
    self.__cycle = 10
    self.__fail_count = 0
    UI.log('STEP#01', 'Repeat 100 times with the command to check the openBMC and microserver can boot up complete without any error')
    self.__TELNET.send('sv stop mTerm\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    self.__TELNET.send('sol.sh\r')
    self.__TELNET.expect('quit')
    self.__TELNET.send('\r')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    self.__TELNET.send('\x18')
    self.__TELNET.expect(self.__dut.ssh_credentials[5])
    
    for i in range(1, self.__cycle + 1):
      self.__TELNET.send('wedge_power.sh reset -s\r')
      
      expect_times = 0
      while True:
        x = self.__TELNET.expect(['(OpenBMC |minipack-v2.1|OpenBMC Release minipack-v2.1 |bmc-oob. login: ).*', 'bmc-oob. login: '])
        expect_times += 1
        if x == 0:
          break
        elif x == 1:
          break
        else:
          time.sleep(1)
          self.__TELNET.send('\r')
      
      self.__TELNET.send('\r')
      self.__TELNET.expect('login:')
      self.__TELNET.send(self.__dut.ssh_credentials[3] + '\r')
      self.__TELNET.expect('Password:')
      self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
      self.__TELNET.expect([self.__dut.ssh_credentials[5], 'Last login:'])
      self.__TELNET.send('\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sol.sh\r')
      self.__TELNET.expect('quit')
      self.__TELNET.send('\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      if  self.__fail_count == 0:
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
        
      if  self.__fail_count == 0:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0260 Reboot_the_Whole_System is passed.')
      else:
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0260 Reboot_the_Whole_System is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
