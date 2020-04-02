#!/usr/bin/python3
# This series of 100 #s defines the width for the content of this document; you should insert line
# breaks when your code exceeds this width. The tab size for this document is set to 2 spaces.
####################################################################################################

import time

from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.pdu import PDU
from lib.cli.facebook.psu import PSU

class FB_Monitor(Script):
	def __init__(self, dut, job_id="", pdu):
		headline = ['Monitor PDU']
		purpose = [
			'To verify the system can get the correct operating status of PDUs and handling the power redundancy currently under different kind of conditions.',
			'The status of PDUs is handling by the CPLD located on PDB card, getting the status is using OpenBMC to read CPLD register through corresponding I2C bus.',
			'Creating the different conditions of power offering on the PDUs, verify the system handle the power redundancy correctly to keep solid operation all the time.']
		
		super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
		super().beginLog()
		
		self.__cycle_count = 1
		self.__sleep_time = 7
			
		self.__pdu = pdu
		self.__fb = dut[1]
		
		self.__PDU_CONNECTION = super().initUI(self.__pdu.telnet_credentials, self.__pdu.platform, PDU)
		self.__TELNET = super().initUI(self.__fb.telnet_credentials, self.__fb.platform, PSU) # TELNET
		# self.__TELNET = super().initUI(self.__fb.console_credentials, self.__fb.platform, PSU) # CONSOLE
		
	def run(self):
		for i in range(1, self.__cycle_count + 1):
			UI.log('STEP#01 - cycle#' + str(i), 'Offer the power to the PDU#1 of the Minipack(Condition #1).', 'The system shall boot up correctly.')
			
			self.__PDU_CONNECTION.powerOff('2, 3, 4')
			
			self.__PDU_CONNECTION.chkPowerStatus('1', 'On')
			self.__PDU_CONNECTION.chkPowerStatus('2, 3, 4', 'Off')
			
			UI.log('STEP#02 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#1 offers the power.')
			
			self.__TELNET.chkPSUStatus('1', 'On')
			self.__TELNET.chkPSUStatus('2, 3, 4', 'Off')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#03 - cycle#' + str(i), 'Offer the power to the PDU#2 of the Minipack(Condition #2).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('2')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2', 'On')
			self.__PDU_CONNECTION.chkPowerStatus('3, 4', 'Off')
			
			UI.log('STEP#04 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#1 and PDU#2 offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2', 'On')
			self.__TELNET.chkPSUStatus('3, 4', 'Off')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#05 - cycle#' + str(i), 'Offer the power to the PDU#3 of the Minipack(Condition #3).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('3')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 3', 'On')
			self.__PDU_CONNECTION.chkPowerStatus('4', 'Off')
			
			UI.log('STEP#06 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#1, PDU#2 and PDU#3 offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2, 3', 'On')
			self.__TELNET.chkPSUStatus('4', 'Off')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#07 - cycle#' + str(i), 'Offer the power to the PDU#4 of the Minipack(Condition #4).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('4')
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 3, 4', 'On')
			
			UI.log('STEP#08 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, all PDUs offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2, 3, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#09 - cycle#' + str(i), 'Terminate the power offering to the PDU#1 of the Minipack(Condition #5).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOff('1')
			
			self.__PDU_CONNECTION.chkPowerStatus('1', 'Off')
			self.__PDU_CONNECTION.chkPowerStatus('2, 3, 4', 'On')
			
			UI.log('STEP#10 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#2, PDU#3 and PDU#4 offer the power.')
			
			self.__TELNET.chkPSUStatus('1', 'Off')
			self.__TELNET.chkPSUStatus('2, 3, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#11 - cycle#' + str(i), 'Terminate the power offering to the PDU#2 of the Minipack(Condition #6).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOff('2')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2', 'Off')
			self.__PDU_CONNECTION.chkPowerStatus('3, 4', 'On')
			
			UI.log('STEP#12 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#3 and PDU#4 offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2', 'Off')
			self.__TELNET.chkPSUStatus('3, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#13 - cycle#' + str(i), 'Terminate the power offering to the PDU#3 of the Minipack(Condition #7).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOff('3')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 3', 'Off')
			self.__PDU_CONNECTION.chkPowerStatus('4', 'On')
			
			UI.log('STEP#14 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#4 offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2, 3', 'Off')
			self.__TELNET.chkPSUStatus('4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#15 - cycle#' + str(i), 'Offer the power offering to the PDU#1 and PDU#2 of the Minipack(Condition #8).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('1, 2')
			
			self.__PDU_CONNECTION.chkPowerStatus('3', 'Off')
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 4', 'On')
			
			UI.log('STEP#16 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#1, PDU#2 and PDU#4 offer the power.')
			
			self.__TELNET.chkPSUStatus('3', 'Off')
			self.__TELNET.chkPSUStatus('1, 2, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#17 - cycle#' + str(i), 'Terminate the power offering to the PDU#1 and PDU#2 of the Minipack(Condition #9).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('1, 2')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 3', 'Off')
			self.__PDU_CONNECTION.chkPowerStatus('4', 'On')
			
			UI.log('STEP#18 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#4 offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2, 3', 'Off')
			self.__TELNET.chkPSUStatus('4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#17 - cycle#' + str(i), 'Offer the power offering to the PDU#1, PDU#2 and PDU#3 of the Minipack(Condition #10).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('1, 2, 3')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 3, 4', 'On')
			
			UI.log('STEP#18', 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented and all PDU offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2, 3, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#19 - cycle#' + str(i), 'Terminate the power offering to the PDU#2 and PDU#3 of the Minipack(Condition #11).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOff('2, 3')
			
			self.__PDU_CONNECTION.chkPowerStatus('2, 3', 'Off')
			self.__PDU_CONNECTION.chkPowerStatus('1, 4', 'On')
			
			UI.log('STEP#20', 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#1 and PDU#4 offer the power.')
			
			self.__TELNET.chkPSUStatus('2, 3', 'Off')
			self.__TELNET.chkPSUStatus('1, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#21 - cycle#' + str(i), 'Offer the power offering to the PDU#3 of the Minipack(Condition #12).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('3')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 3, 4', 'On')
			
			UI.log('STEP#22 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented and all PDU offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2, 3, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#23 - cycle#' + str(i), 'Terminate the power offering to the PDU#3 and PDU#4 of the Minipack(Condition #13).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOff('3, 4')
			
			self.__PDU_CONNECTION.chkPowerStatus('3, 4', 'Off')
			self.__PDU_CONNECTION.chkPowerStatus('1, 2', 'On')
			
			UI.log('STEP#24 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented, but only the PDU#1 and PDU#2 offer the power.')
			
			self.__TELNET.chkPSUStatus('3, 4', 'Off')
			self.__TELNET.chkPSUStatus('1, 2', 'On')
			
			time.sleep(self.__sleep_time)
			
			# ===============
			
			UI.log('STEP#25 - cycle#' + str(i), 'Offer the power offering to the PDU#3 and PDU#4 of the Minipack(Condition #14).', 'The system shall operate steady.')
			
			self.__PDU_CONNECTION.powerOn('3, 4')
			
			self.__PDU_CONNECTION.chkPowerStatus('1, 2, 3, 4', 'On')
			
			UI.log('STEP#26 - cycle#' + str(i), 'Check the status of all PDUs through the OpenBMC.', 'The all PDUs shall be presented and all PDU offer the power.')
			
			self.__TELNET.chkPSUStatus('1, 2, 3, 4', 'On')
			
			time.sleep(self.__sleep_time)
			
	def stop(self):
		 self.__PDU_CONNECTION.close(close_cmd='quit')
		 self.__TELNET.close()
		 
		 super().endLog()