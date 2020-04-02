#!/usr/bin/python3
####################################################################################################

from datetime import datetime
from lib.ui import UI

class SSHv2(UI):
	def __init__(self, ui_credentials, platform):
		super().__init__(ui_credentials, platform=platform)

	# Define your API below this line.

	def setGenerateKey(self, encryption_type=""):
		prompt = super().getPrompt()
		UI.log('ACTION', 'Generate SSH public host key.')
		start = datetime.now()
		timeout = 180
		self.send('ip ssh crypto host-key generate '+encryption_type+'\r')
		self.expect(prompt, timeout=timeout)
		end = datetime.now()
		duration = str(end-start)
		UI.log('Key generation duration: '+duration)

	def showPublicKey(self):
		prompt = super().getPrompt()
		UI.log('ACTION', 'Display SSH public host key.')
		self.send('show public host\r')
		self.expect(prompt)
