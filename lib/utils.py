#!/usr/bin/python3
######################################################################################################################################################
"""Module Name: utils.py
Purpose: General Utility Methods

Description:
  This module implements common utility methods shared across all hosts and platforms. 

Copyright(c) Accton Technology Corporation, 2019
"""

import linecache
import os
import re
import sys
from lib import settings
from lib.ui import UI
  
class Host_Utils(UI):
  def __init__(self, ui_credentials=('host',), platform=settings.host_os):
    super().__init__(ui_credentials, platform=platform)

  def scp(self, copy_direction, src, dst, remote_ip, username, password):
    if re.match('(?i)remote.*host', copy_direction):
      src = username + '@' + remote_ip + ':' + src
    elif re.match('(?i)host.*remote', copy_direction):
      dst = username + '@' + remote_ip + ':' + dst

    EOF = self.getEOF()
    copy_result = 'CHECK'
    copy_msg = ['Command not executed.']

    try:
      self.spawn('scp ' + src + ' ' + dst)

      while True:
        i = self.expect([
          '(?i)password.*',
          '100%.*',
          '(?i)Error opening file',
          '(?i)are the same file',
          '(?i)Permission denied',
          EOF])

        if i == 0:
          self.send(password + '\r')
        elif i == 1:
          copy_result = 'PASS'
          copy_msg[0] = 'File copied successfully.'
          copy_msg.append('Source: ' + src)
          copy_msg.append('Destination: ' + dst)
        elif i == 2:
          copy_result = 'FAIL'
          copy_msg[0] = 'Error copying file.'
        elif i == 3:
          copy_result = 'CHECK'
          copy_msg[0] = 'No file copied.'
        elif i == 4:
          copy_result = 'FAIL'
          copy_msg[0] = 'Invalid username/password.'
        elif i == 5:
          break

    except Exception as e:
      UI.log(str(e))
      copy_result = 'FAIL'
      copy_msg[0] = 'Exception encountered while copying.'

    UI.log(copy_result, *copy_msg)

csv_file_count = 0

def csv2ini(src, dst='', line_break='\r', indent='  ', init_indent_count=0):
  global csv_file_count

  if dst == '':
    dst = src.replace('.csv', '')
    dst = dst + '.ini'

  if os.path.isdir(src):
    section_identifier = src.split('/')[-1]
  else:
    section_identifier = src.split('/')[-1].replace('.csv', '')
    print('Converting ' + src)
    csv_file_count += 1

  init_ind = indent * init_indent_count

  if os.path.exists(dst) and init_indent_count != 0:
    dst_f = open(dst, "a")
  else:
    dst_f = open(dst, 'w')

  dst_f.write(init_ind + '[' + section_identifier + ']' + line_break)

  if os.path.isdir(src):
    dst_f.close()

    for f in os.listdir(src):
      csv2ini(src + '/' + f, dst=dst, init_indent_count=init_indent_count+1)

    return
  else:
    dst_f.write(line_break)

  src = open(src)
  l_list = src.readlines()
  src.close()
  keys = []
  values = []
  keys_count = 0
  prev_l = ''

  for l in l_list:
    l = l.strip(' \r\n;')

    if keys == []:
      keys = l.split(',')
      key_count = len(keys)
      continue

    if prev_l != '':
      l = prev_l + '; ' + l

    if l.count(',') < key_count - 1:
      prev_l = l
      continue
    else:
      values = l.split(',')
      prev_l = ''

    section = values[0].strip('\r\n')
    dst_f.write(init_ind + indent + '['+section+']'+line_break)

    for i in range(1, len(keys)):
      key = keys[i].strip(' \r\n')
      value = values[i].strip(' \r\n')

      if key != '':
        dst_f.write(init_ind + 2 * indent + key + '=' + value + line_break)

    dst_f.write(line_break)

  dst_f.close()

def ini2csv(src_filename, dst_filename, line_break='\r'):
  src = open(src_filename)
  l_list = src.readlines()
  src.close()
  keys_vals = {}
  sections = []
  table = []
  identifier = ''

  re_blank = re.compile('^$')
  #re_section = re.compile('\[([^_]*)_(.*)\]')
  re_section = re.compile('\[(.*)\]')
  re_key_val = re.compile('(.*)=(.*$)')

  for l in l_list:
    l = l.strip(' \r\n')

    for pattern in (re_blank, re_section, re_key_val):
      m = pattern.match(l)

      if m:
        if pattern == re_blank:
          continue
        elif pattern == re_section:
          if identifier == '':
            identifier = m.group(1).strip()
            continue

          sections.append(m.group(1).strip())

          if keys_vals != {}:
            table.append(keys_vals)
            keys_vals = {}

        elif pattern == re_key_val:
          keys_vals[m.group(1).strip()] = m.group(2).strip()

        break

  keys = list(table[0].keys())
  dst = open(dst_filename, 'w')
  dst.write(identifier)

  for k in keys:
    dst.write(',' + k)

  dst.write(line_break)

  for row in table:
    dst.write(sections[0])
    sections = sections[1:]

    for k in keys:
      dst.write(',' + row[k])

    dst.write(line_break)

  dst.close()

def printException():
  exc_type, exc_obj, tb = sys.exc_info()
  f = tb.tb_frame
  lineno = tb.tb_lineno
  filename = f.f_code.co_filename
  linecache.checkcache(filename)
  line = linecache.getline(filename, lineno, f.f_globals)
  print('Exception in {}, line {} "{}":\n{}'.format(filename, lineno, line.strip(), exc_obj))
