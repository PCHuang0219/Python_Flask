#!/usrusr/bin/python3
####################################################################################################

import re
from lib.ui import UI

class System_Mgmt(UI):
	def __init__(self, ui_credentials, platform):
		super().__init__(ui_credentials, platform=platform)

	def showVersion(self):
		UI.log('ACTION', 'Show system version information.')
		prompt = super().getPrompt()
		self.send('show version\r')
		self.expect(prompt)
		UI.log('The system version is displayed above.')
