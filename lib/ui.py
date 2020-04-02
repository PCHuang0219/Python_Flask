#!/usr/bin/python3
######################################################################################################################################################
"""Module Name: ui.py
Purpose: DUT user interface module

Description:
  This module is part of the lib package providing class methods for using console, Telnet, SSH, and SNMP management sessions between the
  workstation and DUT. It also provides logging methods for printing terminal output to the log file and the screen. The UI class is the base class
  for library modules containing APIs for executing DUT test procedures.

Copyright(c) Accton Technology Corporation, 2019
"""

#from __future__ import print_function
import builtins as __builtin__
import sys
import re
import serial
import pexpect
from lib import settings
from pexpect_serial import SerialSpawn
from pysnmp import hlapi

if not 'settings.host_os' in globals():
  settings.init()

# Check operating  system.
if settings.host_os == 'windows':
  import pexpect_for_winpexpect
  from winpexpect import winspawn

class UI():
  """Class Name: UI
  Purpose
    Provides DUT command line user interface and terminal output/logging features.
  """

  log_stream = sys.stdout
  log_terminal_output = True
  end_msg = True
  last_ui = ''
  test_result = 'CHECK'

  def __init__(self, credentials, platform):
    self.__platform = platform
    self.__dut = None
    self.__prompt = ''
    self.__type = credentials[0].lower()
    self.__last_buff = ''
    self.__out_even = True

    if not settings.glb.show_login:
      UI.log_terminal_output = False

    if self.__type == 'host':
      if platform == 'windows':
        self.__EOF = pexpect_for_winpexpect.EOF
        self.__TIMEOUT = pexpect_for_winpexpect.TIMEOUT
      else:
        self.__EOF = pexpect.EOF
        self.__TIMEOUT = pexpect.TIMEOUT

      return
    elif self.__type == 'snmp':
      self.__dut_ip = credentials[1]
      self.__snmp_ver = credentials[2]
      return
    elif self.__type == 'console':
      self.__EOF = pexpect.EOF
      self.__TIMEOUT = pexpect.TIMEOUT
      login_status = self.__initserial__(*credentials[1:])
    elif 'telnet' in self.__type or 'ssh' in self.__type:
      if settings.host_os == 'windows':
        self.__EOF = pexpect_for_winpexpect.EOF
        self.__TIMEOUT = pexpect_for_winpexpect.TIMEOUT
      else:
        self.__EOF = pexpect.EOF
        self.__TIMEOUT = pexpect.TIMEOUT

      if 'telnet' in self.__type:
        login_status = self.__inittelnet__(*credentials[1:])
      elif 'ssh' in self.__type:
        login_status = self.__initssh__(*credentials[1:])

    if login_status == 'PASS':
      if self.__platform == 'simba':
        self.send('terminal length 0\r')
        self.expect(self.__prompt)
        self.send('terminal width '+str(settings.glb.log_width)+'\r')
        self.expect(self.__prompt)

      self.__last_buff = self.getBuff()
      UI.log_terminal_output = True
      self.__init = True
      return self.__dut

    elif login_status == 'FAIL':
      self.__init = False
      self.__dut = None
      self.__prompt = ''
      self.__type = ''
      return self.__dut

  def __setas__(self, other):
    self.__type = other.__type
    self.__dut = other.__dut
    self.__prompt = other.__prompt
    self.__last_buff = other.__last_buff
    self.__EOF = other.__EOF
    self.__TIMEOUT = other.__TIMEOUT
    self.__init = other.__init

  def __initserial__(self, com_port, speed, user, pwd, prompt):
    m = re.match('COM([0-9]+)', com_port)

    if m and settings.host_os == 'linux':
      com_num = m.group(1)
      com_port = '/dev/ttyS'+com_num

    self.__ui_str = 'console '+com_port+' baud rate '+str(speed)
    UI.log('ACTION', 'Initializing '+self.__ui_str)

    try:
      ser = serial.Serial(com_port, speed, timeout=0.1)
      self.__dut = SerialSpawn(ser, timeout=10, encoding='utf-8')
    except Exception as e:
      if not settings.glb.print_to_stdout:
        sys.stdout.write('CRITICAL ALERT: Serial spawn session failed to initialize')
        sys.stdout.write('Please check console login credentials, and verify the COM port is available.')
        sys.stdout.write(e)

      UI.log('CRITICAL ALERT', 'Serial spawn session failed to initialize',
        'Please check console login credentials, and verify the COM port is available.', str(e))

      return 'FAIL'

    self.__prompt = prompt
    return self.__login__(user, pwd)

  def __inittelnet__(self, ip, port, user, pwd, prompt):
    if port != '':
      self.__ui_str = 'Telnet '+ip+' on port '+port
    else:
      self.__ui_str = 'Telnet '+ip

    UI.log('ACTION', 'Initializing '+self.__ui_str)

    try:
      if settings.host_os == 'windows':
        if port != '':
          spw = winspawn('bin_win32/plink -telnet '+ip+' -P '+port)
        else:
          spw = winspawn('bin_win32/plink -telnet '+ip)
          #spw = winspawn('bin_win32/telnet_win.exe '+ip)

      else:
        spw = pexpect.spawn('telnet '+ip+' '+port, encoding='utf-8')

    except Exception as e:
      if not settings.glb.print_to_stdout:
        sys.stdout.write('CRITICAL ALERT: Telnet spawn session failed to initialize')
        sys.stdout.write('Please check Telnet login credentials, and verify the IP address is configured '
          +'properly.')

        sys.stdout.write(e)

      UI.log('CRITICAL ALERT', 'Telnet spawn session failed to initialize',
        'Please check Telnet login credentials, and verify the IP address is configured properly.',
        str(e))

      return 'FAIL'

    self.__dut = spw
    self.__prompt = prompt
    return self.__login__(user, pwd)

  def __initssh__(self, ip, port, user, pwd, prompt):
    if port != '':
      self.__ui_str = 'SSH '+user+'@'+ip+' on port '+port
    else:
      self.__ui_str = 'SSH '+user+'@'+ip

    UI.log('ACTION', 'Initializing '+self.__ui_str)

    try:
      if settings.host_os == 'windows':
        if port != '':
          spw = winspawn('bin_win32/plink -ssh '+user+'@'+ip+' -P '+port)
        else:
          spw = winspawn('bin_win32/plink -ssh '+user+'@'+ip)

      else:
        spw = pexpect.spawn('ssh ' + user + '@' + ip + ' -p ' + port + ' -o StrictHostKeyChecking=no -o ServerAliveInterval=60', encoding='utf-8')

    except Exception as e:
      if not settings.glb.print_to_stdout:
        sys.stdout.write('CRITICAL ALERT: SSH spawn session failed to initialize')
        sys.stdout.write('Please check SSH login credentials, and verify the IP address is configured '
          +'properly.')

        sys.stdout.write(e)

      UI.log('CRITICAL ALERT', 'SSH spawn session failed to initialize',
        'Please check SSH login credentials, and verify the IP address is configured properly.',
        str(e))

      return 'FAIL'

    self.__dut = spw
    self.__prompt = prompt
    return self.__login__(user, pwd)

  def __login__(self, user, pwd):
    if 'ssh' in self.__type and settings.host_os == 'windows':
      return_char = '\n'
    else:
      return_char = '\r'

    if not settings.glb.show_login and user != '' and pwd != '':
      UI.log('Logging in with username/password: '+user+'/'+pwd)

    login_count = 0
    status = ''

    try:
      # if 'telnet' in self.__type:
      #   self.send('')
      # else:
        # self.send('\r')
      self.send('\r')

      while True:
        i = self.expect(['(Username|Login|sonic login|bmc-oob. login: ).*', '(?i)password.*', '(?i)note:',
          self.__prompt, '(?i)permission denied', 'y/n'], timeout=10)
        if i == 3:
          status = 'PASS'
          break
        elif i == 0:
          self.send(user+return_char)
        elif i == 1:
          self.send(pwd+return_char)
          login_count += 1
        elif i == 2:
          if self.__type == 'console':
            self.send('\r')
        elif i == 5:
          self.send('y'+return_char)

        if login_count > 2:
          if not settings.glb.print_to_stdout:
            sys.stdout.write('CRITICAL ALERT: %s Login failed. Permission denied for username/password: %s/%s'
              %(self.__type.capitalize(), user, pwd))

          UI.log('CRITICAL ALERT', '%s Login failed. Permission denied for username/password: %s/%s'
            %(self.__type.capitalize(), user, pwd))

          status = 'FAIL'
          break

      if not settings.glb.show_login:
        UI.log('LOGIN SUCCESS', str(self)+' is initialized.')

      if status == 'FAIL':
        self.__dut.close()

      return status

    except self.__EOF:
      UI.log_stream.write(self.getBuff())

      if not settings.glb.print_to_stdout:
        sys.stdout.write('CRITICAL ALERT: %s login failed; please check login credentials.'
            %self.__type.capitalize())

      UI.log('CRITICAL ALERT', '%s login failed; please check login credentials.'
          %self.__type.capitalize())

    except self.__TIMEOUT:
      UI.log_stream.write(self.getBuff())

      if not settings.glb.print_to_stdout:
        sys.stdout.write('CRITICAL ALERT: %s login timed out; please check login credentials.'
          %self.__type.capitalize())

      UI.log('CRITICAL ALERT', '%s login timed out; please check login credentials.'
        %self.__type.capitalize())

  def getOutEven(self):
    return self.__out_even

  def init(self):
    return self.__init

  def getPrompt(self):
    return self.__prompt

  def getEOF(self):
    return self.__EOF

  def getTIMEOUT(self):
    return self.__TIMEOUT

  def close(self, close_cmd='exit'):
    if self.__dut is None:
      return

    if not settings.glb.show_login:
      UI.log('LOGGING OUT', 'Closed ' + self.__ui_str)
      UI.log_terminal_output = False

    try:
      self.send(settings.glb.ctrl_c)
      self.expect(self.__prompt, writting = None)
      self.send(close_cmd + '\r')

      while True:
        i = self.expect([self.__EOF,
            '(?i)(note:|login|exit session).*',
            self.__prompt], writting = None)

        if i == 0 or i == 1:
          break
        elif i == 2:
          self.send(close_cmd + '\r')

    except:
      if self.__dut.isalive():
        self.__dut.terminate()

    if self.__dut != None:
      self.__dut.close()

    if UI.log_terminal_output:
      UI.log('Closed ' + self.__ui_str)

    self.__dut = None
    self.__type = None
    self.__init = False
    UI.log_terminal_output = True
    return None

  def spawn(self, *cmd):
    try:
      if settings.host_os == 'windows':
        self.__ui_str = 'Windows host CMD'
        self.__dut = winspawn(*cmd)
      elif settings.host_os == 'linux':
        self.__ui_str = 'Linux host Bash shell'
        self.__dut = pexpect.spawn(*cmd, encoding='utf-8')

      cmd = ''.join(*cmd)
      UI.log('ACTION', 'Executing command on ' + self.__ui_str, 'Command: ' + cmd)
      UI.logTitle('TERMINAL OUTPUT from '+self.__ui_str)
      UI.last_ui = str(self)
      last_line = self.__last_buff.split('\n')[-1]
      UI.log_stream.write(last_line)

      if settings.glb.print_to_stdout:
        sys.stdout.write(last_line)

      UI.end_msg = False
    except Exception as e:
      if not settings.glb.print_to_stdout:
        sys.stdout.write('CRITICAL ALERT: Host spawn session failed to initialize')
        sys.stdout.write(str(e))

      UI.log('CRITICAL ALERT', 'Host spawn session failed to initialize', str(e))
      self.__dut = None

  def send(self, *args):
    if self.__dut == None:
      return

    if (UI.end_msg or UI.last_ui != str(self)) and UI.log_terminal_output:
      UI.log_stream.write(settings.glb.change_line)
      UI.logTitle('TERMINAL OUTPUT from '+self.__ui_str)
      UI.last_ui = str(self)
      last_line = self.__last_buff.split('\n')[-1]
      UI.log_stream.write(last_line)

      if settings.glb.print_to_stdout:
        sys.stdout.write(last_line)

    UI.end_msg = False
    return self.__dut.send(*args)

  def sendWithoutOutput(self, *args):
    if self.__dut == None:
      return
    else:
      return self.__dut.send(*args)

  def expect(self, *args, timeout = 10, writting = True, before=True, after=True):
    self.__out_even = False
    expectError = False

    if self.__dut == None:
      return

    try:
      ret = self.__dut.expect(*args, timeout=timeout)
    except:
      expectError = True
      ret = 1
      pass

    if writting:
      buff = self.getBuff(before=before, after=after)
      if UI.log_terminal_output:
        UI.log_stream.write(buff)

        if settings.glb.print_to_stdout:
          sys.stdout.write(buff)
        

      else:
        UI.end_msg = True

      if args[0][ret] == self.__EOF:
        UI.last_ui = ''
        self.__dut = None
        self.__last_buff = ''
      else:
        self.__last_buff = buff

    self.__out_even = True
    if expectError:
      return 100
    else:
      return ret

  def getBuff(self, before=True, after=True):
    if self.__dut == None:
      return ''

    ret_str = ''

    if 'str' in str(type(self.__dut.before)) and before:
      ret_str = self.__dut.before

    if 'str' in str(type(self.__dut.after)) and after:
      ret_str += self.__dut.after

    return ret_str

  def getLastBuff(self):
    return self.__last_buff

  def getBeforeBuff(self):
    if 'str' in str(type(self.__dut.before)):
      return self.__dut.before
    else:
      return "NULL"

  def getAfterBuff(self):
    if 'str' in str(type(self.__dut.after)):
      return self.__dut.after
    else:
      return "NULL"

  def sendCmd(self, cmd, prompt = "", writting=True, timeout=10):
    if prompt == "":
      prompt = self.__prompt
    self.send(cmd+'\r')
    ret = self.expect(prompt, writting=writting, timeout=timeout)
    if ret == 0 :
      return self.getOutputFromLastBuff(cmd, prompt=prompt)
    else:
      return ""
  
  def getOutputFromLastBuff(self, cmd, prompt = ""):
    if prompt == "":
      prompt = self.__prompt
    relist = self.getBuff().splitlines()
    retstr = ""
    for line in relist:
      if not re.search('^\x1b]0;root.*', line):
        if cmd != line:
          retstr += line + '\n'
    return retstr

  def snmpGet(self, oids, credentials='', port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    target = self.__dut_ip

    if self.__snmp_ver.lower() == '2c':
      credentials = hlapi.CommunityData('public')

    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context, 
        *construct_object_types(oids)
    )

    ret = fetch(handler, 1)[0]
    ret_list = []

    for key, value in ret.items():
      temp = key + ': ' + value
      ret_list.append(temp)

    UI.log('SNMP-GET', 'Remote IP: ' + self.__dut_ip, *ret_list)
    return ret

  def snmpSet(self, value_pairs, credentials='', port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    target = self.__dut_ip

    if self.__snmp_ver.lower() == '2c':
      credentials = hlapi.CommunityData('private')

    handler = hlapi.setCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_value_pairs(value_pairs)
    )

    ret = fetch(handler, 1)[0]
    ret_list = []

    for key, value in ret.items():
      temp = key + ': ' + value
      ret_list.append(temp)

    UI.log('SNMP-SET', 'Remote IP: ' + self.__dut_ip, *ret_list)
    return ret

  @classmethod
  def openLog(class_object, filename):
    UI.log_stream = open(filename, 'a')

  @classmethod
  def logTitle(class_object, title):
    if not UI.end_msg:
      UI.log_stream.write(settings.glb.change_line)

      if settings.glb.print_to_stdout:
        sys.stdout.write('\n')

    centered_title = '{:=^{w}}'.format(' '+title+' ', w=settings.glb.log_width)
    UI.log_stream.write(centered_title)

    if settings.glb.print_to_stdout:
      sys.stdout.write(centered_title)

    UI.log_stream.write(settings.glb.change_line)
    UI.end_msg = True

    if settings.glb.print_to_stdout:
      sys.stdout.write('\n\n')

    if title == 'PASS' and UI.test_result == 'CHECK':
      UI.test_result = 'PASS'
    elif title == 'FAIL':
      UI.test_result = 'FAIL'

  @classmethod
  def log(class_object, *msg):
    if not UI.end_msg:
      UI.log_stream.write(settings.glb.change_line)

      if settings.glb.print_to_stdout:
        sys.stdout.write('\n')

    if msg[0].isupper():
      title = msg[0]
      msg = msg[1:]
      UI.logTitle(title)
    else:
      divider = '='*settings.glb.log_width
      UI.log_stream.write(divider)
      UI.log_stream.write(settings.glb.change_line)

      if settings.glb.print_to_stdout:
        sys.stdout.write(divider)
        sys.stdout.write('\n\n')

    first_word = msg[0].split(' ')[0]

    if re.match('(\.|:)', first_word[-1]):
      indent = ' '*(len(first_word)+1)
    else:
      indent = ''

    for m in msg:
      # Perform word wrap for each line of message.
      m.strip('\n')
      lines = ''
      word_list = str(m).split(' ')

      for w in word_list:
        last_line = (lines+w).split('\n')[-1]

        if len(last_line) > settings.glb.log_width:
          lines += '\n'+indent+w+' '
        else:
          lines += w+' '

      UI.log_stream.write(lines+'\n')

      if settings.glb.print_to_stdout:
        sys.stdout.write(lines+'\n')

    if settings.glb.print_to_stdout:
      sys.stdout.write('\n')

    UI.end_msg = True

  @classmethod
  def closeLog(class_object):
    UI.log_stream.write('\n\n')
    UI.log_stream.close()
    f = open(UI.log_stream.name, 'r')
    l_list = f.readlines()
    f.close()
    new_f = open(UI.log_stream.name, 'w')
    empty_line_count = 0

    for l in l_list:
      l = l.replace(']0;root@minipack:~', '')
      if re.search('^[\r\n]+$', l, re.M) or len(l) == 1:
        empty_line_count += 1
      else:
        if empty_line_count > 2:
          new_f.write('\n')

        new_f.write(l)
        empty_line_count = 0

    new_f.close

def construct_object_types(list_of_oids):
  object_types = []

  for oid in list_of_oids:
    object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))

  return object_types

def fetch(handler, count):
  result = []

  for i in range(count):
    try:
      error_indication, error_status, error_index, var_binds = next(handler)

      if not error_indication and not error_status:
        items = {}

        for var_bind in var_binds:
          items[str(var_bind[0])] = cast(var_bind[1])

        result.append(items)
      else:
        raise RuntimeError('Got SNMP error: {0}'.format(error_indication))

    except StopIteration:
      break

  return result

def cast(value):
  try:
    return int(value)
  except (ValueError, TypeError):
    try:
      return float(value)
    except (ValueError, TypeError):
      try:
        return str(value)
      except (ValueError, TypeError):
        pass

  return value

def construct_value_pairs(list_of_pairs):
  pairs = []

  for key, value in list_of_pairs.items():
    pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))

  return pairs

def myPrint(msg):
  UI.log_stream.write(str(msg) + '\n')

  if UI.log_stream != sys.stdout:
    sys.stdout.write(str(msg) + '\n')

__builtins__['print'] = myPrint
