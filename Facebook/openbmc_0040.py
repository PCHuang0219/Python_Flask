#!/usr/bin/python3
####################################################################################################

import re
from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.openbmc import OpenBMC

class OpenBMC_0040(Script):
  def __init__(self, dut, job_id="", image_server = 'None'):
    # Modify headline and purpose to describe your script.
    # Enclose strings using single quotes ''.
    # Surround assignment operator = with spaces.
    headline = ['Monitoring Temperature Sensor']

    purpose = [
        'To verify the temperature sensors for Inlet Temp, Switch Temp, Outlet Temp and Microserver Ambient Temp can be accessed.',
			'The following commands can be used:',
			'1. cat /sys/bus/i2c/drivers/lm75/*/hwmon/*/temp1_input',
			'The temperature sensor values, reported as degrees Celsius * 1000. So 28500 is 28.5C.',
			'2. sensors tmp75-*.']

    self.__dut = dut[1]
    super().__init__(headline, purpose, script_path=__file__,job_id=job_id)
    # Start logging the script.
    super().beginLog()

  def run(self):
    """
    Function Name: run
    Purpose: Executes the steps defined by this test case.
    """

    # initialize serial, Telnet and SSH UI with SystemMgmt APIs.
    self.__SSH = super().initUI(self.__dut.ssh_credentials, self.__dut.platform,OpenBMC)
    self.__cycle = 1
    self.__bais = 200
    self.__fail_count = 0
    self.__sensors = ['tmp75-i2c-3-48', 'tmp75-i2c-3-49', 'tmp75-i2c-3-4a', 'tmp75-i2c-3-4b',
        'tmp75-i2c-51-48', 'tmp75-i2c-52-49', 'tmp75-i2c-59-48', 'tmp75-i2c-60-49', 'tmp75-i2c-66-48', 'tmp75-i2c-66-49',
        'tmp75-i2c-74-48', 'tmp75-i2c-74-49', 'tmp75-i2c-82-48', 'tmp75-i2c-83-4b', 'tmp75-i2c-90-48', 'tmp75-i2c-91-4b','tmp75-i2c-98-48', 'tmp75-i2c-99-4b',
        'tmp75-i2c-106-48', 'tmp75-i2c-107-4b', 'tmp75-i2c-114-48', 'tmp75-i2c-115-4b', 'tmp75-i2c-122-48', 'tmp75-i2c-123-4b',
        'tmp75-i2c-130-48', 'tmp75-i2c-131-4b', 'tmp75-i2c-138-48', 'tmp75-i2c-139-4b']

    # Do not surround assignment operator = with spaces in paranthesised expressions.
    for i in range(1, self.__cycle + 1):
        for sensor in self.__sensors:
            sensor_id = re.search('(?i)tmp75-i2c-(.*)', sensor)
            sensor_id_1 = sensor_id.group(0).split('-')[2]
            sensor_id_2 = sensor_id.group(0).split('-')[3].zfill(4)
				
			# ==================================================================================================
            UI.log('STEP#01 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use the command "cat /sys/bus/i2c/drivers/lm75/*/…" to monitor the sensors.')
            self.__SSH.send('cat /sys/bus/i2c/drivers/lm75/' + sensor_id_1 + '-' + sensor_id_2 +'/hwmon/hwmon*/temp1_input\r')
            self.__SSH.expect("#")

            cat_result = re.search('(?i)No such file or directory', self.__SSH.getBuff(), re.M)
            temperature = self.__SSH.getBuff().splitlines()[1]
	
            if cat_result != None:
                UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': ' + sensor + ' is inexistent.')
            else:
                # ==================================================================================================
                UI.log('STEP#02 - cycle#' + str(i) + '/' + str(self.__cycle), 'Use the command "sensors tmp75-*" to monitor the sensors.')
                self.__SSH.send('sensors ' + sensor + '\r')
                self.__SSH.expect("#")
					
                temperature_sensor = re.search('(?i)\+([0-9.]+) C', self.__SSH.getBuff(), re.M)
                temperature_correct = int(float(temperature_sensor.group(1)) * 1000)
	
				# ==================================================================================================
                UI.log('STEP#03 - cycle#' + str(i) + '/' + str(self.__cycle), 'To compare the values.')
                if abs(temperature_correct - int(temperature)) < 200:
                    UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': ' + sensor + ' comapare pass.', 'The bais is ' + str(self.__bais))
                else:
                    self.__fail_count += 1

                    UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': ' + sensor + ' comapare fail.', 'The bais is ' + str(self.__bais))

    if self.__fail_count == 0:
        UI.log('PASS', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0040 Monitoring_Temperature_Sensor is passed.')
    else:
        UI.log('FAIL', 'Cycle#' + str(i) + '/' + str(self.__cycle) + ': BMC_0040 Monitoring_Temperature_Sensor is failed.')

  def stop(self):
    # Terminate interfaces and restore settings.
    self.__SSH.close()
    # Stop logging the script.
    super().endLog()