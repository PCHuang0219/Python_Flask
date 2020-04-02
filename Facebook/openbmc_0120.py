#!/usr/bin/python3
####################################################################################################

import re
import time
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0120(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    headline = ['Update whole BMC flash']
		purpose = [
			'scp flash-minipack root@<bmc-ip-addr>:/tmp',
			'flashcp -v flash-minipack /dev/mtd5',
			'Then, reboot the system for the new firmware to take effect.']
		expect_result = [
			'OpenBMC can be upgrade without any error.']

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
    self.__cycle = 1
		self.__sleep_time = 15
		self.__bmc_run_ver = 'formal'

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    for i in range(1, self.__cycle + 1):
			# ==================================================================================================
			UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Set an IP for BMC eth0.')
			self.__TELNET.send('sudo ifconfig eth0 ' + self.__dut.ssh_credentials[1] + ' netmask ' + self.__dut.ssh_netmask + ' \r')
			self.__TELNET.expect(self.__dut.ssh_credentials[5])
			
			# ==================================================================================================
			UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use scp funtion to copy openBMC image to BMC then check the image is transfer correctlly.')
			new_bmc_ver = self.__TELNET.getImageVersion(self.image_server.local_new_image_path + '/OpenBMC/' + self.__bmc_run_ver + '/version.txt')
			new_bmc_filename = self.__TELNET.getImageFilename(self.image_server.local_new_image_path + '/OpenBMC/' + self.__bmc_run_ver + '/version.txt')
			
			UI.log('OpenBMC(' + new_bmc_filename + ') New version is "' + new_bmc_ver + '".')
			
			server_file_path = self.image_server.local_new_image_path.replace(self.image_server.local_root_path, '') + '/OpenBMC/' + self.__bmc_run_ver + '/' + new_bmc_filename
			
			self.__TELNET.downloadFile(self.__fb.scp_server_username, self.__fb.scp_server_password, self.__fb.scp_server_ip,
				server_file_path, '/var/tmp/minipack_flash')
				
			# ==================================================================================================
			UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'Update BMC flash and reset the system when after update complete.')
			self.__TELNET.send('flashcp -v /var/tmp/minipack_flash /dev/mtd5\r')
			
			while True:
				if self.__TELNET.expect([self.__dut.ssh_credentials[5], '%'], timeout=180) == 0:
					break
					
			self.__TELNET.send('wedge_power.sh reset -s\r')
			
			while True:
        x = self.__TELNET.expect(['(OpenBMC |minipack-v2.1|OpenBMC Release minipack-v2.1 |bmc-oob. login: ).*', 'bmc-oob. login: '])
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
			
			# ==================================================================================================
			UI.log('STEP#04 - cycle#' + str(i) + '/' + str(self.__cycle), 'Verify the version is correct.')
			self.__TELNET.send('cat /etc/issue\r')
			self.__TELNET.expect(self.__dut.ssh_credentials[5])
			
			result = re.search('(?i)' + new_bmc_ver, self.__TELNET.getBuff(), re.M)
			
			if result == None:
				UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': OpenBmc version is NOT match!!')
				UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0120 Update_whole_BMC_flash is failed.')
			else:
				UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': OpenBmc version is match!!')
				UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0120 Update_whole_BMC_flash is passed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__TELNET.close()
    # Stop logging the script.
    super().endLog()