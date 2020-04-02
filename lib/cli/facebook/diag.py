#!/usr/bin/python3
####################################################################################################

from datetime import datetime
from lib.ui import UI
import time

class Diag(UI):
	def __init__(self, ui_credentials, platform):
		super().__init__(ui_credentials, platform=platform)

	# Define your API below this line.

	def runDiagTest(self, itemint, testType, caseName):
		self.prompt = super().getPrompt()
		caseName = caseName.replace('_', ' ')
		UI.log('ACTION', 'Execute diag test: ' + caseName)
		result = 'FAIL'
		cmd = 'python /usr/local/accton/bin/diag_api.py ' + itemint + ' ' + testType + '\r'
		breakEven = False
		breakForloop = False

		self.send(cmd)
		while True:
			x = self.expect([self.prompt, '\n', '^0:_soc_cmicx_schan_wait:', 'bcmLINK.0', '^Please.* $'])
			if x == 0 :
				break
			elif x >=2 and x <=3:
				self.send('\x03')
				result = 'FAIL'
				break
			elif x == 4:
				min_number = int(self.getAfterBuff().split('-')[0][-1])
				max_number = int(self.getAfterBuff().split('-')[1][0])
				for i in range(min_number,max_number + 1):
					if breakForloop:
						result = 'FAIL'
						break
					if i > min_number:
						result = self.runDiagTestAgain(cmd, result, str(i))
					else:
						self.sendCmd(str(i))
						while True:
							x = self.expect([self.prompt, '\n'],timeout=0.5)
							if x == 0:
								break
							if x == 100:
								breakForloop = True
								breakEven = True
								break
					if i == max_number:
						breakEven = True
			if breakEven:
				break
			if 'PASSED' in self.getBuff():
				result = 'PASS'

		if result == 'PASS' :
			UI.log('PASS', 'Minipack Diag test: ' + caseName + ' is PASS.')
		else:
			UI.log('FAIL', 'Minipack Diag test: ' + caseName + ' is FAIL.')

	def runDiagTestAgain(self, cmd, result, parameter):
		self.send(cmd)
		while True:
			x = self.expect([self.prompt, '\n', '^0:_soc_cmicx_schan_wait:', 'bcmLINK.0', '^Please.* $'],timeout=3)
			if x == 0:
				break
			elif x == 4:
				self.sendCmd(parameter)

			if 'FAILED' in self.getBuff():
				result = 'FAIL'
		
		return result