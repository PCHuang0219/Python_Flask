#!/usr/bin/python3
####################################################################################################
"""Module Name: facebook.py
Copyright(c) Accton Technology Corporation, 2019
"""

from lib.ui import UI

class FPGA(UI):
    def __init__(self, ui_credentials, platform):
      super().__init__(ui_credentials, platform=platform)
    
    @classmethod
    def chk_string(class_obj, str_get, str_expect):
        if str_expect.lower() in str_get.lower():
          UI.log('PASS', 'The string '+str_expect+' is found in'+ str_get + '.')

        else:
          UI.log('FAIL', 'The string '+str_expect+' is not found in '+ str_get + '.')

    def minicycle_raw(self, offset, check_value, way):
        """Function Name: minicycle_raw
        Purpose: Read the raw data by tool mimicycle

        Input:
        offset - offset to read
        check_value - Value to check 

        Examples:

        History: 2019/09/24 - Romeo Lo, created.
        """
        prompt = super().getPrompt()
        UI.log('Get IOB ID and check if it is correct.')
        if way == "read":
            UI.log('ACTION', 'Read the raw data by tool mimicycle')
            self.send('addison/minicycle/minicycle.py -raw ' + offset + '\r')
            self.expect(prompt)
            buff = self.getBuff()
            self.chk_string(buff, check_value)
            
        elif way == "write":
            UI.log('ACTION', 'Write the raw data by tool mimicycle')
            self.send('addison/minicycle/minicycle.py -raw ' + offset + ' ' + check_value + '\r')
            self.expect(prompt)
            buff = self.getBuff()
            
        elif way == "get":
            UI.log('ACTION', 'Get the raw data by tool mimicycle')
            self.send('addison/minicycle/minicycle.py -raw ' + offset +'\r')
            self.expect(prompt)
            buff = self.getBuff()
            data = buff.split('\n')
            code_ret = data[1].replace('0x', '').replace('\r', '')
            return(code_ret)
    
    def minicycle_rtc(self, pim, leng='', desc='', check_value='' , way='read', offset='' , port=''):
        """Function Name: minicycle_raw
        Purpose: Read the raw data by tool mimicycle

        Input:
        pim - PIM number
        port - port number
        offset - offset to read
        leng - data length
        desc - descriptor
        check_value - Value to check 
        way - Which way to do, read, write or get

        Examples:

        History: 2019/09/24 - Romeo Lo, created.
        """
        cmd_line = 'addison/minicycle/minicycle.py -rtc pim=' + pim
        if port != "":
            cmd_line = cmd_line + ' port=' + port
        if offset != "":
            cmd_line = cmd_line + ' offset=' + offset
        if leng != "":
            cmd_line = cmd_line + ' leng=' + leng
        if desc != "":
            cmd_line = cmd_line + ' desc=' + desc
        
        if check_value != "":
            cmd_line = cmd_line + " " + check_value
        
        cmd_line = cmd_line + ' \r'
            
        prompt = super().getPrompt()
        if way == "read":
            UI.log('ACTION', 'Read the rtc data by tool mimicycle')
            self.send(cmd_line)
            self.expect(prompt)
            buff = self.getBuff()
            self.chk_string(buff, check_value)
        elif way == "write":
            UI.log('ACTION', 'Write the rtc data by tool mimicycle')
            self.send(cmd_line)
            self.expect(prompt)
            buff = self.getBuff()
        elif way == "get":
            UI.log('ACTION', 'Get the rtc data by tool mimicycle')
            self.send(cmd_line)
            self.expect(prompt)
            buff = self.getBuff()
            data = buff.split('\n')
            # code_ret = data[1].replace('0x', '').replace('\r', '')
            return(data)

    def minicycle_mdio(self, pim, leng='', desc='', check_value='' , way='read', offset='' , port='', phy=''):
            """Function Name: minicycle_raw
            Purpose: Read the raw data by tool minicycle

            Input:
            pim - PIM number
            port - port number
            offset - offset to read
            leng - data length
            desc - descriptor
            check_value - Value to check 
            way - Which way to do, read, write or get

            Examples:

            History: 2019/09/24 - Romeo Lo, created.
            """
            
            import time
            cmd_line = 'addison/minicycle/minicycle.py -mdio pim=' + pim
            if port != "":
                cmd_line = cmd_line + ' port=' + port
            if offset != "":
                cmd_line = cmd_line + ' offset=' + offset
            if leng != "":
                cmd_line = cmd_line + ' leng=' + leng
            if desc != "":
                cmd_line = cmd_line + ' desc=' + desc
            if phy != "":
                cmd_line = cmd_line + ' phy=' + phy
                
            if check_value != "" and way == 'write':
                cmd_line = cmd_line + " " + check_value
            
            cmd_line = cmd_line + ' \r'
                
            # prompt = self.dut.getPrompt()
            prompt = '~]#'
            print('command line is ' + cmd_line)
            if way == "read":
                UI.log('ACTION', 'Read the mdio data by tool minicycle')
                self.send(cmd_line)
                time.sleep(10)
                self.expect(prompt)
                buff = self.getBuff()
                code_ret = buff.replace('| ', '')
                self.chk_string(code_ret, check_value)
                
            elif way == "write":
                UI.log('ACTION', 'Write the mdio data by tool minicycle')
                self.send(cmd_line)
                self.expect(prompt)
                buff = self.getBuff()
                print(buff)
                
                
            elif way == "get":
                print('get')
                UI.log('ACTION', 'Get the mdio data by tool minicycle')
                self.send(cmd_line)
                self.expect(prompt)
                buff = self.getBuff()
                data = buff.split('\n')
                return(data)
    
def generate_rand_hex():
    import random
    ran = random.randrange(0,4294967295)
    myhex = hex(ran)
    return myhex
    

def hex_2_32bin(input_hex):
    # return format(int(input_hex), '0>32b')
    import math 
  
    # Initialising hex string 
    ini_string = input_hex
      
    # Printing initial string 
    print ("Initial string" + ini_string) 
      
    # Code to convert hex to binary 
    res = "{0:032b}".format(int(ini_string, 32)) 
      
    # Print the resultant string 
    print ("Resultant string" + str(res)) 
    return str(res)

def hex_2_dec(input_hex):
    # return format(int(input_hex), '0>32b')
    import math 
  
    # Initialising hex string 
    ini_string = input_hex
      
    # Printing initial string 
    print ("Initial string is : " + ini_string) 
      
    # Code to convert hex to binary 
    res = int(ini_string, 16)
      
    # Print the resultant string 
    print ("Resultant string is : " + str(res)) 
    return str(res)

def gen_bin_byport(port, reverse='false'):
    # Given the port number and get the binary format
    new_str = ""
    if reverse == 'true':
      bin_value = '0'
      other_value = '1'
    else:
      bin_value = '1'
      other_value = '0'
    for num in range(1,17):
      if num in port:
        new_str = bin_value + new_str
      else:
        new_str = other_value + new_str
    return new_str

def ByteToHexwith0x( byteStr ):
    return '0x' + ' 0x'.join( [ "%02X" % ord( x ) for x in byteStr ] )
    
def ByteToHex( byteStr ):
    return ' '.join( [ "%02X" % ord( x ) for x in byteStr ] )