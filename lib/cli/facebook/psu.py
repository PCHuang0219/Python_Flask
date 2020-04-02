#!/usr/bin/python3
####################################################################################################

import re

from lib.ui import UI

class PSU(UI):
	def __init__(self, ui_credentials, platform):
		super().__init__(ui_credentials, platform=platform)
		
	def chkPSUStatus(self, index_list, status):
		"""
		Check PSU status(on, off or shutdown)
		
		Attributes:
			index - PSU sensor index
			status - PSU status: On / Off / shutdown
		"""
	
		prompt = super().getPrompt()
		
		UI.log('ACTION', 'Check PSU status.')
		
		for index in index_list.split(','):
			index = index.strip()
			
			self.send('sensor-util psu' + index + ' --force\r')
			self.expect(prompt)
			
			if status.lower() == 'on':
				result = re.search('(?i)PSU' + str(index) + '_IN_VOLT [ ]+ \(0x[0-9A-Za-z]+\) :[ 0-9.]+ Volts \| \(ok\)', self.getBuff())
				
				if result == None:
					UI.log('FAIL', 'The power of PSU' + str(index) + ' shall be ON.')
				else:
					UI.log('PASS', 'The power of PSU' + str(index) + ' is "ON"')
			elif status.lower() == 'off':
				result = re.search('(?i)PSU' + str(index) + '_IN_VOLT [ ]+ \(0x[0-9A-Za-z]+\) :( ?)NA \| \(na\)', self.getBuff())
				
				if result == None:
					UI.log('FAIL', 'The power of PSU' + str(index) + ' shall be OFF.')
				else:
					UI.log('PASS', 'The power of PSU' + str(index) + ' is "OFF"')
			elif status.lower() == 'shutdown':
				result = re.search('(?i)psu' + str(index) + ' is not present!', self.getBuff())
				
				if result == None:
					UI.log('FAIL', 'The power of PSU' + str(index) + ' shall be SHUTDOWN.')
				else:
					UI.log('PASS', 'The power of PSU' + str(index) + ' is "SHUTDOWN"')