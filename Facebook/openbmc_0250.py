#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0250(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Access BMC from Microserver via ssh']
    purpose = ['To verify BMC can be successfully accessed from microserver via ssh.']

    self.__dut = dut[1]
    self.image_server = image_server
    self.__comE_eth0_ip = dut[0].ssh_credentials[1]
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
    self.__cycle = 1
    self.__fail_count = 0
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01- cycle#' + str(i) + '/' + str(self.__cycle), 'Set an IP for BMC eth0.')
      self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + '\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Set a IP for COM-e diag eth0.')
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sol.sh\r')
      self.__TELNET.expect('quit.')
      self.__TELNET.send('\r')
      self.__TELNET.expect('~]# ')
      self.__TELNET.send('sudo ifconfig eth0 ' + self.__comE_eth0_ip + ' netmask ' + self.__dut.ssh_netmask + '\r')
      self.__TELNET.expect('~]# ')
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'SSH to BMC from COM-e diag.')
      self.__TELNET.send('ssh ' + self.__dut.ssh_credentials[1]  + '\r')
      
      while True:
        result = self.__TELNET.expect([self.__dut.ssh_credentials[5], '~]# ', '\(yes/no\)?', 'password:'], timeout= 180) 
        
        if result == 0:
          UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': SSH connection success.')
        
          self.__TELNET.send('exit\r')
          self.__TELNET.expect('~]# ')
        
          break
        elif result == 1:
          self.__fail_count += 1
          
          UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': SSH connection failure.')
          
          break
        elif result >= 2:
          if  result == 2:
            self.__TELNET.send('yes\r')
            self.__TELNET.expect('password:')
            
          self.__TELNET.send(self.__dut.ssh_credentials[4] + '\r')
          
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
    if self.__fail_count == 0:
      UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0250 Access_BMC_ from_Microserver_via_ssh is passed.')
    else:
      UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0250 Access_BMC_ from_Microserver_via_ssh is failed.')
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
        
      if  self.__fail_count == 0:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0260 Reboot_the_Whole_System is passed.')
      else:
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0260 Reboot_the_Whole_System is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
