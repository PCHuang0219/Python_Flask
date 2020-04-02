#!/usr/bin/python3
####################################################################################################

from lib.ui import UI
# Import your need library below this line.

class SONiC_API(UI):
  def __init__(self, ui_credentials, platform):
    super().__init__(ui_credentials, platform=platform)
    self.prompt = super().getPrompt()

	# Define your API below this line.
  def changeImageVersion(self, url):
    UI.log("ACTION", "Install SONiC image from " + url)
    cli = 'sudo sonic_installer install -y ' + url + '\r'
    self.send(cli)
    while True:
      x = self.expect(['\r', self.prompt])
      if x == 1 :
        UI.log("PASS", "Install SONiC image success.")
        # Upgrade finished.
        break
