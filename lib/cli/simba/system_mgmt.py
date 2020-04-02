#!/usr/bin/python3
######################################################################################################################################################

import re
import time
from lib.ui import UI
from lib.settings import CopyFile_settings

cp = CopyFile_settings()

class System_Mgmt(UI):
  def __init__(self, ui_credentials, platform):
    super().__init__(ui_credentials, platform=platform)

  # Define your API below this line.

  def shutDownPort(self, port_list, action='enable'):
    """Function Name: shutDownPort
    Purpose: Shutdown or no-shutdown Eethernet port.

    Input:
      port_list - list of Ethernet port in 'unit/number' format; for example ['1/1', '1/10']
      action - 'shutdown' to shutdown or 'no-shutdown' to no-shutdown the port.

    Examples:
      shutDownPort(port_list = ['1/1'], action = 'shutdown)
      shutDownPort(port_list = ['1/1', 1/3', 1/11', 1/15'], action = 'no-shutdown')

    History: 2019/06/06 - Michael Chen, created.
    """

    prompt = self.getPrompt()

    if 'no' not in action:
      UI.log('ACTION', 'Shutting down the following ports:', *port_list)
      cmd = 'shutdown\r'
    else:
      UI.log('ACTION', 'No-shutting down the following ports:', *port_list)
      cmd = 'no shutdown\r'

    self.send('config\r')
    self.expect(prompt)

    for port in port_list:
      self.send('inter ether '+port+'\r')
      self.expect(prompt)
      self.send(cmd)
      self.expect(prompt)
      self.send('exit\r')
      self.expect(prompt)

    self.send('end\r')
    self.expect(prompt)

  def chkPortStatus(self, port_list, status='enable'):
    """Function Name: chkPortStatus
    Purpose: Checks if a port is shutdown or no-shutdown.

    Input:
      port_list - list of Ethernet port in 'unit/number' format; for example ['1/1', '1/10']
      status - 'no-shutdown' or 'shutdown'

    Examples:
      chkPortStatus(port_list = ['1/1'], status = 'shutdown')
      chkPortStatus(port_list = ['1/1', 1/3', 1/11', 1/15'], status = 'no-shutdown')

    History: 2019/06/10 - Michael Chen, created.
    """

    prompt = self.getPrompt()
    UI.log('ACTION', 'Verify the following ports have status '+status+'.', *port_list)

    # Prepare regular expression for port list.
    # Join list of port numbers with the '|' or character.
    re_port_list = '|'.join(port_list)

    # Insert a check for 0 or 1 spaces ' ?' after the '/' to account for ports less than 10.
    re_port_list = re_port_list.replace('/', '/ ?')

    self.send('show inter brief\r')
    self.expect(prompt)
    buff = self.getBuff()

    # Find all strings matching the list of ports and their port statuses in the buffer.
    found_list = re.findall('(?i)^eth ('+re_port_list+') +(up|down|disable)', buff, re.M)

    for f_port, f_display in found_list:
      # Remove space in port number.
      f_port = f_port.replace(' ', '')

      if f_display.lower() == 'down' or f_display.lower() == 'up':
        f_status = 'no-shutdown'
      else:
        f_status = 'shutdown'

      if f_status == status:
        UI.log('PASS', 'The Ethernet port '+f_port+' status is correct: '+f_status+'.')
      elif f_status != status:
        UI.log('FAIL', 'The Ethernet port '+f_port+' status is incorrect.',
          'Expected: '+status+'; found: '+f_status+'.')

  def showSystemInfo(self):
    prompt = super().getPrompt()
    UI.log('ACTION', 'Get system information.')
    self.send('show system\r')
    self.expect(prompt)
    UI.log('The system information is shown above.')

  def chkSystemModel(self, model_name, log_terminal_output=True):
    prompt = super().getPrompt()
    UI.log('ACTION', 'Check system model name.')
    UI.log_terminal_output = log_terminal_output
    self.send('show system\r')
    self.expect(prompt)
    buff = self.getBuff()
    match = re.search('^.*'+model_name, buff, re.M)

    if match:
      UI.log('PASS', 'The model name is found.', match.group(0))
    else:
      UI.log('FAIL', 'The model name "'+model_name+'" is not found.')

    UI.log_terminal_output = True
  def copyFileFile(self, src_file, dst_file, check='success'):
    prompt = super().getPrompt()
    UI.log('ACTION', 'Copy "'+src_file+'" as "'+dst_file+'".')
    self.send('copy file file\r')
    copy_result = ''
    while True:
      i = self.expect([
        cp.src_re,
        cp.dst_re,
        cp.confirm_re,
        cp.pass_re,
        cp.fail_re,
        cp.busy_re,
        cp.timeout_re,
        prompt])

      if i == 0:
        self.send(src_file+'\r')
      elif i == 1:
        self.send(dst_file+'\r')
      elif i == 2:
        self.send('y\r')
      elif i == 3:
        copy_result = 'success'
      elif i == 4:
        copy_result = 'fail'
      elif i == 5:
        copy_result = 'busy'
      elif i == 6:
        copy_result = 'timeout'
      elif i == 7:
        break

    fd = ('Source file: '+src_file, 'Destination file: '+dst_file)

    if copy_result == check:
      UI.log('PASS', 'File copy result matches criteria.', fd[0], fd[1], 'Copy result: '+copy_result)
    else:
      UI.log('FAIL', 'File copy result does not match criteria.', fd[0], fd[1], 'Copy result: '+copy_result)

  def copyFileInterrupt(self, src, dst, ui_2, check='success'):
    """Method Name: copyFileInterrupt
    Purpose: Attempts to perform two copy file operations simultaneously.

    Input Parameters:
      src - source file description; [tftp, tftp_ip, config/op, src_name]
      dst - destination file description; [file, dst_name]
      ui_2 - second UI session.
      check - expected copy result
    """

    prompt = super().getPrompt()
    second_copy = False
    self.send('copy '+src[0]+' '+dst[0]+'\r')

    expect_list=[
    # 0
      '(?i)power source.*',
    # 1
      '(?i)(y or n|y/n).*',
    # 2
      '(?i)public key type.*',
    # 3
      '(?i)copy.*which unit.*',
    # 4
      '(?i)choose file type.*',
    # 5
      '(?i)source.*file name.*',
    # 6
      '(?i)(startup|destination).*file name.*',
    # 7
      '(?i)server ip address.*',
    # 8
      '(?i)username.*',
    # 9
      '(?i)password.*',
    # 10
      '(?i)startup configuration file name.*',
    # 11
      '(?i)flash programming started.*',
    # 12
      '(?i)Timeout.*',
    # 13
      '(?i)(invalid|no such|file not|usbdisk is not ready|error|cannot be\
      replaced|fail).*',
    # 14
      '(?i)same.*not updated.*',
    # 15
      '(?i)success.*',
    # 16
      prompt,
    # 17
      '/'
    ] #end expect_list

    copy_result = 'none'
    last_buff = ''

    while True:
      i = self.expect(expect_list, timeout=60)

      if i == 7:
        if re.match('[0-9]+\.[0-9]+\.[0-9]+\.[0-9]', src[1]):
          self.send(src[1]+'\r')
        else:
          self.send(dst[1]+'\r')

      elif i == 4:
        if 'config' in src:
          self.send('1\r')
        elif 'op' in src:
          self.send('2\r')

      elif i == 5:
        self.send(src[-1]+'\r')
      elif i == 6:
        self.send(dst[-1]+'\r')
      elif i == 14 or i == 15:
        copy_result = 'success'
      elif i == 12:
        copy_result = 'timeout'
      elif i == 13:
        copy_result = 'failed'
      elif i == 17:
        if not second_copy:
          ui_2.copyFileFile(src_file=cp.default_config, dst_file='test', check='busy')
          second_copy = True
          time.sleep(0.2)
          self.send('')

        UI.log_terminal_output = False

      if copy_result != 'none' and UI.log_terminal_output == False:
        UI.log_stream.write(self.getBuff())
        UI.log_terminal_output = True
        UI.end_msg = False

      if i == 16:
        UI.log_terminal_output = True
        print(copy_result+'\n')
        break

    fd = ('Source file: '+src[-1], 'Destination file: '+dst[-1])

    if copy_result == check:
      UI.log('PASS', 'File copy result matches criteria.', fd[0], fd[1], 'Copy result: '+copy_result)
    else:
      UI.log('FAIL', 'File copy result does not match criteria.', fd[0], fd[1], 'Copy result: '+copy_result)
