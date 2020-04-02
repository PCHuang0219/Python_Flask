#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0210(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['File copy - From Microserver']
    purpose = ['To verify BMC can copy a directory of files from Microserver.']

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
    self.__cycle = 1
    self.__fail_count = 0
    for i in range(1, self.__cycle + 1):
      # ==================================================================================================
      UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'To unload the g_serial module.')
      self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + ' \r')
			self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('ps | grep usbmon.sh\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)usbmon.sh', self.__TELNET.getBuff(), re.M)
      
      if result != None:
        self.__TELNET.send('killall usbmon.sh\r')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
        
      self.__TELNET.send('ps | grep getty\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)getty', self.__TELNET.getBuff(), re.M)
      
      if result != None:
        self.__TELNET.send('killall getty\r')
        self.__TELNET.expect(self.__dut.ssh_credentials[5])
        
      self.__TELNET.send('modprobe -r g_cdc\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Create an image and load g_mass_storage module.')
      self.__TELNET.send('dd if=/dev/zero of=/var/volatile/image bs=1M count=16\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('modprobe g_mass_storage file=/var/volatile/image stall=0\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sv stop mTerm\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('sol.sh\r')
      self.__TELNET.expect('quit')
      self.__TELNET.send('\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Create a folder and a file named ntc and named test_019_File_copy.txt under the COM-e diag.')
      self.__TELNET.send('cd /\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('mkdir ntc\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cd /ntc\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('vi test_019_File_copy.txt\r')
      time.sleep(2)
      self.__TELNET.send('a')
      time.sleep(2)
      self.__TELNET.send('for BMC_0210_File_copy_From_Microserver test')
      time.sleep(2)
      self.__TELNET.send('\x1b')
      time.sleep(2)
      self.__TELNET.send('\x1b')
      time.sleep(2)
      self.__TELNET.send(':wq\r')
      time.sleep(2)
      self.__TELNET.send('\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cd ..\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'zip the folder to this device on Microserver.')
      self.__TELNET.send('tar c /ntc/ > /dev/sdb\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cd ..\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#05 - cycle#' + str(i) + '/' + str(self.__cycle), 'Press "Ctrl+x" to exit diag and to the path.')
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cd /var/volatile/\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#06 - cycle#' + str(i) + '/' + str(self.__cycle), 'Unzip image.')
      self.__TELNET.send('tar xvf image\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('cat ntc/test_019_File_copy.txt\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      result = re.search('(?i)for BMC_0210_File_copy_From_Microserver test', self.__TELNET.getBuff(), re.M)
      
      if result == None:
        self.__fail_count += 1
        
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The File can not be copied from COM-e to BMC.')
      else:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': The File can be copied from COM-e to BMC.')
        
      self.__TELNET.send('cd ..\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      # ==================================================================================================
      UI.log('STEP#07 - cycle#' + str(i) + '/' + str(self.__cycle), 'SOL to COM-e and remove the folder.')
      self.__TELNET.send('sol.sh\r')
      self.__TELNET.expect('quit')
      self.__TELNET.send('\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('rm -rf /ntc/\r')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      self.__TELNET.send('\x18')
      self.__TELNET.expect(self.__dut.ssh_credentials[5])
      
      if self.__fail_count == 0:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0210 File_copy_From_Microserver is passed.')
      else:
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0210 File_copy_From_Microserver is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()
