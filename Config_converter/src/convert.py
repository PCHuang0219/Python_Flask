    #!/usr/bin/python3
######################################################################################################################################################
"""Module Name: convert.py
Purpose: Test Module for csv<->ini Converter

Description:
  This module demonstrates the functionality of the bi-directional csv-ini conversion utility. This script can convert a single csv file into an ini
  file, and can also convert a database containing csv files stored within a directory tree into a single ini file with the sections, sub-sections,
  sub-sub-sections, ... representing the original nested folders/files directory structure. Finally, the script can convert a ini file with a single
  [section][key] level data structure back into a  corresponding csv file witht the sections as rows and keys as columns.

Author: Michael Chen <michael_chen@accton.com>
Copyright(c) Accton Technology Corporation, 2019
"""

import os
import re
import sys
from datetime import datetime

def csv2ini(src, dst='', line_break='\r', indent='  ', init_indent_count=0):
  global file_count

  if dst == '':
    dst = src.replace('.csv', '')
    dst = dst + '.ini'

  if os.path.isdir(src):
    section_identifier = src.split('/')[-1]
  else:
    section_identifier = src.split('/')[-1].replace('.csv', '')
    print('Converting ' + src)
    file_count += 1

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

if len(sys.argv) == 1:
  print('Please enter a source file path as the first argument.')
  exit

src = sys.argv[1]

if len(sys.argv) == 2:
  dst = src
  m = re.match('([0-9-]{10}_[^_]+_)', dst)

  if m:
    dst = dst.replace(m.group(1), '')

  time_stamp = str(datetime.now()).split('.')[0].replace(' ', '_')
  time_stamp = time_stamp.replace('', '')
  time_stamp = time_stamp.replace(':', '')
  dst = time_stamp + '_' + dst
else:
  dst = sys.argv[2]

if 'csv' in src.lower() or os.path.isdir('csv/' + src):
  if len(sys.argv) == 2:
    dst = dst.replace('.csv', '')
    dst = dst + '.ini'

  print('Creating ini file: ' + dst)
  file_count = 0
  csv2ini('csv/' + src, 'ini/' + dst)

  if file_count > 1:
    print(str(file_count) + 'files converted.\n')
  else:
    print(str(file_count) + 'file converted.\n')

elif 'ini' in src.lower():
  if len(sys.argv) == 2:
    dst = dst.replace('.ini', '.csv')

  print('Creating csv file: ' + dst + '\n')
  ini2csv('ini/' + src, 'csv/' + dst)
else:
  print('Invalid command, please try again.')
