#!/usr/bin/python3
####################################################################################################

import time
import re

from lib.ui import UI

class PDU(UI):
	def __init__(self, ui_credentials, platform):
		super().__init__(ui_credentials, platform=platform)
		
		self.__sleep_time = 1
		
	def powerReboot(self, number_list, model='ATEN'):
		prompt = super().getPrompt()
		
		if model == 'ATEN':
			UI.log('ACTION', 'Power REBOOT outlet number "' + number_list + '".')
			
			for number in number_list.split(','):
				number_format = str('%02d' % int(number.strip()))
				
				self.send('sw o' + number_format + ' reboot\r')
				time.sleep(self.__sleep_time)
				self.expect(prompt)
				
				time.sleep(self.__sleep_time)
		
	def powerOn(self, number_list, model='ATEN'):
		prompt = super().getPrompt()
		
		if model == 'ATEN':
			UI.log('ACTION', 'Power ON outlet number "' + number_list + '".')
			
			for number in number_list.split(','):
				number_format = '%02d' % int(number.strip())
				
				self.send('sw o' + number_format + ' on imme\r')
				time.sleep(self.__sleep_time)
				self.expect(prompt)
				
				time.sleep(self.__sleep_time)
		
	def powerOff(self, number_list, model='ATEN'):
		prompt = super().getPrompt()
		
		if model == 'ATEN':
			UI.log('ACTION', 'Power OFF outlet number "' + number_list + '".')
			
			for number in number_list.split(','):
				number_format = str('%02d' % int(number.strip()))
				
				self.send('sw o' + number_format + ' off imme\r')
				time.sleep(self.__sleep_time)
				self.expect(prompt)
				
				time.sleep(self.__sleep_time)
		
	def chkPowerStatus(self, number_list, status, model='ATEN'):
		prompt = super().getPrompt()
		
		if model == 'ATEN':
			UI.log('CHECK', 'Check Power ' + number_list + ' status.')
			
			for number in number_list.split(','):
				number_format = str('%02d' % int(number.strip()))
				
				self.send('read status o' + number_format + ' format\r')
				time.sleep(self.__sleep_time)
				self.expect(prompt)
				
				time.sleep(self.__sleep_time)
			
				result = re.search('(?i)Outlet ' + number_format + ' ' + status, self.getBuff())
				
				if result == None:
					UI.log('FAIL', 'Power ' + number + ' status shall be "' + status + '".')
				else:
					UI.log('PASS', 'Power ' + number + ' status is correct.')