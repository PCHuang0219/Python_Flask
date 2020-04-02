#!/usr/bin/python3
####################################################################################################
"""
Module Name: system_0010.py
Purpose    : Execute system-0010 test case

Description:
  There are two necessary parameter :
            - dut            : the DUT object on which testing is performed.

History     :
    Anber Huang 12/20/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""

from lib.ui import UI
from lib.script import Script
from lib.cli.facebook.system import System
from lib.cli.facebook.parameters import *
import time
import re

class System_0010(Script):
  def __init__(self,dut, job_id):
    headline = ['Stress test CP2112']

    purpose = ['Combine diagnostic test item :',
                '       4. The probe test cp2112 for usb-to-i2c bus',
                '     104. Show QSFP EEPROM through CP2112',
                '     107. The simple test for show QSFP EEPROM through CP2112']

    self.__COMe = dut[0]
    self.__BMC = dut[1]

    self.__COMe_prompt = self.__COMe.ssh_credentials[5]
    self.__BMC_prompt = self.__BMC.ssh_credentials[5]
    super().__init__(headline, purpose, script_path=__file__, job_id=job_id)
    super().beginLog()
    self.__COMe_SSH = super().initUI(self.__COMe.ssh_credentials, self.__COMe.platform, System)
    self.__BMC_SSH = super().initUI(self.__BMC.ssh_credentials, self.__BMC.platform, System)
    # Start logging the script.

  def run(self):
    # ### DIAG item : 159 ###
    # UI.log('ACTION', 'The Test for FPGA I2C High-Speed Path START')
    # retstr = self.__COMe_SSH.sendCmd('python /usr/local/accton/bin/diag_api.py 159 normal', timeout=60).splitlines()
    # if "PASS" in  retstr[-2]:
    #   UI.log('PASS', 'The Test for FPGA I2C High-Speed Path is PASS !')
    # else:
    #   UI.log('FAIL', 'The Test for FPGA I2C High-Speed Path is FAIL !')

    # ## DIAG item : 4 ###
    # UI.log("ACTION", "Get i2c device address from COMe session")
    # i2c_0_device_address = self.__COMe_SSH.i2cBusTest()
    # try_count = 0
    # self.ret = DIAG_STATUS_SUCCESS
    # UI.log("ACTION", "While loop to read device address")
    # while try_count < MAXIMUM_CP2112_RETRY:
    #   try:
    #     ## Register
    #     self.__BMC_SSH.set_cp2112_rst(1)
    #     self.__COMe_SSH.check_cp2112_exist(True)

    #     ## Unregister
    #     self.__BMC_SSH.set_cp2112_rst(0)
    #     self.__COMe_SSH.check_cp2112_exist(False)

    #     ## Register
    #     self.__BMC_SSH.set_cp2112_rst(1)
    #     self.__COMe_SSH.check_cp2112_exist(True)

    #     self.__COMe_SSH.check_i2c_address(i2c_0_device_address)

    #   except Exception as e:
    #     try_count += 1
    #     print(repr(e))
    #     self.ret = DIAG_STATUS_FAILED
    #     return DIAG_STATUS_FAILED
    #   else:
    #     break

    # ### DIAG item : 104 ###
    # UI.log("ACTION", "Show QSFP EEPROM through CP2112")

    # self.__COMe_SSH.send("minipack_transceiver_eeprom.sh -m 0\r")

    # fail_count = 0
    # while True:
    #   time.sleep(1)
    #   x = self.__COMe_SSH.expect([self.__COMe_prompt, '\n\r', '\r'], timeout= 180)
    #   if x == 0:
    #     break
    #   elif "failed" in self.__COMe_SSH.getBuff():
    #     fail_count += 1

    # if fail_count > 0 :
    #   UI.log("FAIL", "Show QSFP EEPROM through CP2112 is FAIL!")
    # else:
    #   UI.log("PASS", "Show QSFP EEPROM through CP2112 is PASS!")

    ## DIAG item : 115 ###
    # UI.log('ACTION', 'Show Revision of CPLD and FPGA START')
    # ret = DIAG_STATUS_SUCCESS
    # rs = ""
    # try:
    #   cpld_ls = {}
    #   fpga_ls = {}
    #   others_ls = {}
    #   board_cfg = self.__COMe_SSH.get_board_config()
    #   if board_cfg & BOARD_SMB:
    #     cpld_ls["SMBCPLD"] = ret
    #     fpga_ls["IOBFPGA"] = ret
    #     if board_cfg & BOARD_PT:
    #       pass
    #     else:
    #       others_ls["POWR1220AT8"] = self.__BMC_SSH.bmc_show_powr1220_rev()
    #       others_ls["IR3595AMTRPBF"] = self.__BMC_SSH.bmc_show_ir3595_rev()
    #   if board_cfg & BOARD_SCM:
    #     cpld_ls["SCMCPLD"] = ret
    #   if board_cfg & BOARD_FCM_ALL:
    #     cpld_ls["Top FCMCPLD"] = ret
    #     cpld_ls["Bottom FCMCPLD"] = ret
    #   if board_cfg & BOARD_PDB_ALL:
    #     cpld_ls["Left PDBCPLD"] = ret
    #     cpld_ls["Right PDBCPLD"] = ret
    #   if board_cfg & BOARD_PIM_ALL:
    #     pim_ls = [PIM_ID_TO_NUM[brd_id] for brd_id in PIM_ID_TO_NUM if brd_id & board_cfg]
    #     for pim_num in pim_ls:
    #       fpga_ls["PIM %d DOMFPGA" % pim_num] = ret

    #   fail_str_ls = ["read error", "0.0", "255.255", "Read failed", "not detected", "not inserted"]

    #   ## Check cpld version ##
    #   for retry in range(4):
    #     if len(cpld_ls) == 0:
    #       break
    #     exist_fail = False
    #     if retry > 0:
    #       print("cpld retry %d" % retry)
    #     rs = self.__BMC_SSH.get_process_result("cpld_ver.sh")
    #     UI.log("------CPLD version------")
    #     for line in rs:
    #       for cpld_name in cpld_ls:
    #         if cpld_name in line:
    #           print(line)
    #           ## Check error message ##
    #           for err in fail_str_ls:
    #             if err in line:
    #               cpld_ls[cpld_name] = DIAG_STATUS_FAILED
    #               exist_fail = True
    #               break
    #     if exist_fail:
    #       continue
    #     else:
    #       break
      
    #   ## Check fpga version ##
    #   for retry in range(4):
    #     if len(fpga_ls) == 0:
    #       break
    #     exist_fail = False
    #     check_next_line = False
    #     last_fpga_name = ""
    #     rs = self.__BMC_SSH.get_process_result("fpga_ver.sh")
    #     if retry > 0:
    #       UI.log("Get FPGA Version %d times" % (retry + 1))
    #     else:
    #       UI.log("Get FPGA Version first times")
    #     for line in rs:
    #       if "FPGA" in line and "-----" in line:
    #         print(line)
    #         exist_fail = True
    #       elif "IOBFPGA" in line:
    #         print(line)
    #         for err in fail_str_ls:
    #           if err in line:
    #             fpga_ls["IOBFPGA"] = DIAG_STATUS_FAILED
    #             exist_fail = True
    #       elif re.match("PIM [1-8]:", line):
    #         pim_str = line.split(":")[0]
    #         for name in fpga_ls:
    #           if pim_str in name:
    #             print(line)
    #             check_next_line = True
    #             last_fpga_name = name
    #             break
    #       elif "DOMFPGA" in line and check_next_line:
    #         print(line)
    #         check_next_line = False
    #         for err in fail_str_ls:
    #           if err in line:
    #             fpga_ls[last_fpga_name] = DIAG_STATUS_FAILED
    #             exist_fail = True
    #             break
    #       if exist_fail:
    #         continue
    #       else:
    #         break

    #     ## Examine result ##
    #     for ls in [others_ls, cpld_ls, fpga_ls]:
    #       for item in ls:
    #         if ls[item] is not DIAG_STATUS_SUCCESS:
    #           UI.log("FAIL", "%s: get version fail !" % item)
    #           ret = DIAG_STATUS_FAILED

    # except Exception as e:
    #     print(repr(e))
    #     print(rs)
    #     return DIAG_STATUS_FAILED

    # return ret

    ### DIAG item : 54 ###
    # UI.log('ACTION', 'Show COM-E HW information START')
#     try:
#       dmistr = self.__COMe_SSH.sendCmd("dmidecode -t 0 -t 1 -t 2 -t 3 -t 4 -t 17")
#     except Exception as e:
#       UI.log("FAIL", "dmidecode(%d): FAIL!" % e.returncode)
#     try:
#       smartstr = self.__COMe_SSH.sendCmd("smartctl -i /dev/sda -d sat")
#     except Exception as e:
#       UI.log("FAIL", "smartctl(%d): FAIL!" % e.returncode)

#     rs = cmd = bic_ver = pvccin_vr = ddrab_vr = p1v05_vr = ''
#     try:
#       cmd = 'fw-util scm --version'
#       rs = self.__BMC_SSH.bmc_check_process_done(cmd, 1, 15, True, 3)
#       assert rs[0] == DIAG_STATUS_SUCCESS
#       bicstr_ls = rs[1].splitlines()
#       assert len(bicstr_ls) > 4
#       for line in bicstr_ls:
#         if 'Bridge-IC Version' in line:
#           bic_ver = line.split(':')[1].strip()
#         elif 'PVCCIN VR Version' in line:
#           pvccin_vr = line.split(':')[1].strip()
#         elif 'DRAB VR Version' in line:
#           ddrab_vr = line.split(':')[1].strip()
#         elif 'P1V05 VR Version' in line:
#           p1v05_vr = line.split(':')[1].strip()
#     except AssertionError:
#       print('%s FAIL!' % cmd)
#       print('Debug:', rs)
#       UI.log("FAIL", "AssertionError")
#     except Exception as e:
#       UI.log("FAIL", "Exception : " + str(e))

    
#     try:
#       cmd = 'bic-util scm --read_fruid'
#       rs = self.__BMC_SSH.bmc_check_process_done(cmd, 1, 15, True, 3)
#       assert rs[0] == DIAG_STATUS_SUCCESS
#       rs_ls = rs[1].splitlines()
#       assert len(rs_ls) > 21
#       UI.log("Print Hardware Information Start")
#       for line in rs_ls:
#         if ':' in line and 'root@' not in line:
#           print(line)
#     except AssertionError:
#       print('%s FAIL!' % cmd)
#       print('Debug:', rs)
#       UI.log("FAIL", "AssertionError")
#     except Exception as e:
#       UI.log("FAIL", "Exception : " + str(e))


#     dmi = dmistr.splitlines()
#     smart = smartstr.splitlines()
#     #ecver = ecverstr.splitlines()

#     for anchor, line in enumerate(dmi):
#       if "BIOS Information" in line:
#         break
#     print("BIOS Vender               : %s" % parse_value(dmi[anchor+1]))
#     print("BIOS Revision             : %s" % parse_value(dmi[anchor+2]))
#     print("BIOS FW Revision          : %s" % parse_value(dmi[anchor+27]))
#     print("BIC Version               : %s" % bic_ver)
#     print("PVCCIN VR Version         : %s" % pvccin_vr)
#     print("DDRAB VR Version          : %s" % ddrab_vr)
#     print("P1V05 VR Version          : %s" % p1v05_vr)


#     for anchor, line in enumerate(dmi):
#         if "System Information" in line:
#             break

#     print("Manufacturer              : %s" % parse_value(dmi[anchor+1]))
#     print("Product Name              : %s" % parse_value(dmi[anchor+2]))
#     #print("Version                  : %s" % parse_value(dmi[anchor+3]))
#     #print("Serial Number            : %s" % parse_value(dmi[anchor+4]))
#     #print("Minilake SN              : %s" % snstr[16])
#     #print("SKU Number               : %s" % parse_value(dmi[anchor+7]))
#     #print("Family                   : %s" % parse_value(dmi[anchor+8]))

#     for anchor, line in enumerate(dmi):
#         if "Base Board Information" in line:
#             break

#     #print("Base Board SN            : %s" % parse_value(dmi[anchor+4]))

#     for anchor, line in enumerate(dmi):
#         if "Chassis Information" in line:
#             break

#     #print("Chassis Manufacturer     : %s" % parse_value(dmi[anchor+1]))
#     #print("Chassis Serial Number    : %s" % parse_value(dmi[anchor+5]))
#     #print("Chassis Asset Tag        : %s" % parse_value(dmi[anchor+6]))

#     for anchor, line in enumerate(dmi):
#         if "Processor Information" in line:
#             break

#     print("CPU Manufacturer          : %s" % parse_value(dmi[anchor+4]))
#     print("CPU Version               : %s" % parse_value(dmi[anchor+36]))
#     print("CPU Clock                 : %s" % parse_value(dmi[anchor+38]))
#     print("CPU Number of Cores       : %s" % parse_value(dmi[anchor+49]))
#     print("CPU Max Speed             : %s" % parse_value(dmi[anchor+39]))

#     for anchor, line in enumerate(dmi):
#         if "DMI type 17, 40 bytes" in line:
# #        if "Memory Device" in line:
#             break

#     print("DIMM_A0 Size              : %s" % parse_value(dmi[anchor+6]))
#     print("DIMM_A0 Factor            : %s" % parse_value(dmi[anchor+7]))
#     print("DIMM_A0 Type              : %s" % parse_value(dmi[anchor+11]))
#     print("DIMM_A0 Speed             : %s" % parse_value(dmi[anchor+13]))
#     print("DIMM_A0 Manufacturer      : %s" % parse_value(dmi[anchor+14]))
#     print("DIMM_A0 SN                : %s" % parse_value(dmi[anchor+15]))
#     print("DIMM_A0 PN                : %s" % parse_value(dmi[anchor+17]))

#     for anchor, line in enumerate(dmi):
#         if "DMI type 17, 40 bytes" in line:
# #        if "Memory Device" in line:
#             break

#     print("DIMM_B0 Size              : %s" % parse_value(dmi[anchor+30]))
#     print("DIMM_B0 Factor            : %s" % parse_value(dmi[anchor+31]))
#     print("DIMM_B0 Type              : %s" % parse_value(dmi[anchor+35]))
#     print("DIMM_B0 Speed             : %s" % parse_value(dmi[anchor+37]))
#     print("DIMM_B0 Manufacturer      : %s" % parse_value(dmi[anchor+38]))
#     print("DIMM_B0 SN                : %s" % parse_value(dmi[anchor+39]))
#     print("DIMM_B0 PN                : %s" % parse_value(dmi[anchor+41])) 

#     for anchor, line in enumerate(smart):
#         if "Device Model" in line:
#             break

#     print("SSD Vender                : %s" % parse_value(smart[anchor]))
#     print("SSD SN                    : %s" % parse_value(smart[anchor+1]))
#     print("SSD FW Version            : %s" % parse_value(smart[anchor+3]))

#     UI.log("PASS", "Show COM-E HW information is PASS !")


  ### DIAG item : 63 ###
    # UI.log('ACTION', 'The stress-ng performance test for CPU START')
    # self.__COMe_SSH.cpu_stress_ng_test()

  ## DIAG item : 11 ###
    # UI.log('ACTION', 'The R/W test for memory device(RAM) START')
    # self.__COMe_SSH.ddr_test()
  
  ### DIAG item : 403 ###
    # UI.log('ACTION', 'Check CPU FPGA pcie error START')
    # ret = self.__BMC_SSH.bmc_check_pcie_err()
    # if ret == DIAG_STATUS_FAILED:
    #   UI.log("FAIL", "Check BMC system event log is FAIL !")
    # else:
    #   UI.log("PASS", "Check BMC system event log is PASS !")

    # ret = self.__COMe_SSH.check_cpu_log()
    # if ret == DIAG_STATUS_FAILED:
    #   UI.log("FAIL", "Check CPU FPGA pcie error is FAIL !")
    # else:
    #   UI.log("PASS", "Check CPU FPGA pcie error is PASS !")

  ### DIAG item : 400 ###
    # UI.log('ACTION', 'Clear all AER mask of all pci devices START')
    # ret = self.__COMe_SSH.pci_all_clear_all_aer_mask()
    # if ret != 0:
    #   UI.log('FAIL', 'Clear all AER mask of all pci devices is FAIL !')
    # else:
    #   UI.log('PASS', 'Clear all AER mask of all pci devices is PASS !')
  
  ### DIAG item : 158 ###
    # UI.log('ACTION', 'TThe Test for FPGA I2C Low-Speed Path QSFP EEPROM START')
    # retstr = self.__COMe_SSH.sendCmd('python /usr/local/accton/bin/system_fpga.py 158').splitlines()
    # for line in retstr:
    #   if re.search('The Test for FPGA I2C Low-Speed Path QSFP EEPROM', line):
    #     if "PASS" in line:
    #       UI.log('PASS', 'The Test for FPGA I2C Low-Speed Path QSFP EEPROM is PASS !')
    #     else:
    #       UI.log('FAIL', 'The Test for FPGA I2C Low-Speed Path QSFP EEPROM is FAIL !')

    ### DIAG item : 159 ###
    # UI.log('ACTION', 'The Test for FPGA I2C High-Speed Path START')
    # retstr = self.__COMe_SSH.sendCmd('python /usr/local/accton/bin/system_fpga.py 159', timeout=60).splitlines()
    # for line in retstr:
    #   if re.search('The Test for FPGA I2C High-Speed Path', line):
    #     if "PASS" in line:
    #       UI.log('PASS', 'The Test for FPGA I2C High-Speed Path is PASS !')
    #     else:
    #       UI.log('FAIL', 'The Test for FPGA I2C High-Speed Path is FAIL !')

    ### DIAG item : 162 ###
    # UI.log('ACTION', 'Check FPGA PCI-E bus error START')
    # self.__COMe_SSH.diag_item_check_fpga_pcie_bus_error()

    ### DIAG item : 156 ###
    # UI.log('ACTION', 'The Test for FPGA MDIO 16Q')
    # self.__COMe_SSH.fpga_mdio_16q_test()
  
    ### DIAG item : 108 ###
    # ret = self.__COMe_SSH.Mcelog_Verify()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_FAILED:
    #   UI.log("FAIL", "Detecting machine check exceptions is FAIL")
    # else:
    #   UI.log("PASS", "Detecting machine check exceptions is PASS")

    ### DIAG item : 150 ###
    # ret = self.__COMe_SSH.th3_xgkr_test()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "The Test of 10G KR CPU<-->TH3 is PASS")
    # else:
    #   UI.log("FAIL", "The Test of 10G KR CPU<-->TH3 is FAIL")

    ### DIAG item : 151 ###
    # UI.log("ACTION", "The Test of 1G SGMII TH3<-->BCM5396")
    # ret = self.__COMe_SSH.th3_mgmt_test()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "The Test of 1G SGMII TH3<-->BCM5396 is PASS")
    # else:
    #   UI.log("FAIL", "The Test of 1G SGMII TH3<-->BCM5396 is FAIL")

    # ### DIAG item : 152 ###
    # UI.log("ACTION", "The Test of 16Q linespeed")
    # ret = self.__COMe_SSH.phy16q_linespeed_test()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "The Test of 16Q linespeed is PASS")
    # else:
    #   UI.log("FAIL", "The Test of 16Q linespeed is FAIL")

    # ### DIAG item : 154 ###
    # UI.log("ACTION", "Dump all serdes info")
    # ret = self.__COMe_SSH.serdes_info_test()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "Dump all serdes info is PASS")
    # else:
    #   UI.log("FAIL", "Dump all serdes info is FAIL")

    # ### DIAG item : 155 ###
    # UI.log("ACTION", "The Test of 16Q 40G linespeed")
    # ret = self.__COMe_SSH.phy16q_40g_linespeed_test()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "The Test of 16Q 40G linespeed is PASS")
    # else:
    #   UI.log("FAIL", "The Test of 16Q 40G linespeed is FAIL")

    # ### DIAG item : 157 ###
    # UI.log("ACTION", "The Test of 16Q 200G linespeed")
    # ret = self.__COMe_SSH.phy16q_200g_linespeed_test()
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "The Test of 16Q 200G linespeed is PASS")
    # else:
    #   UI.log("FAIL", "The Test of 16Q 200G linespeed is FAIL")

    # ### DIAG item : 163 ###
    # UI.log("ACTION", "Check Tomahawk3 PCI-E bus error")
    # ret = self.__COMe_SSH.diag_item_check_th3_pcie_bus_error()
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "Check Tomahawk3 PCI-E bus error is PASS")
    # else:
    #   UI.log("FAIL", "Check Tomahawk3 PCI-E bus error is FAIL")

    # ### DIAG item : 401 ###
    # UI.log("ACTION", "Check if any AER error happened from dmesg")
    # ret = self.__COMe_SSH.check_aer_dmesg("*")
    # self.__COMe_SSH.sendCmd("cd", writting=False)
    # if ret == DIAG_STATUS_SUCCESS:
    #   UI.log("PASS", "Check if any AER error happened from dmesg is PASS")
    # else:
    #   UI.log("FAIL", "Check if any AER error happened from dmesg is FAIL")

    # UI.log('ACTION', 'Check CPU FPGA pcie error START')
    # ret = self.__BMC_SSH.bmc_check_pcie_err()
    # if ret == DIAG_STATUS_FAILED:
    #   UI.log("FAIL", "Check BMC system event log is FAIL !")
    # else:
    #   UI.log("PASS", "Check BMC system event log is PASS !")

    ret = self.__COMe_SSH.check_cpu_log()
    if ret == DIAG_STATUS_FAILED:
      UI.log("FAIL", "Check CPU FPGA pcie error is FAIL !")
    else:
      UI.log("PASS", "Check CPU FPGA pcie error is PASS !")


  def stop(self):
    self.__COMe_SSH.close()
    self.__BMC_SSH.close()

    # Stop logging the script.
    super().endLog()