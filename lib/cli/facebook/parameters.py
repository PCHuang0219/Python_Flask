#!/usr/bin/python3
####################################################################################################
import threading

class MyThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

def parse_value(str):
    return str.partition(':')[2].lstrip()

def txt2tokens(instr, prompt=""):
    strlines = instr.splitlines()
    result = []
    for line in strlines:
        if prompt not in line:
            result.append(line.split())
    return result

# Configuration options
CONFIG_FACEBOOK_VERSION = False
CONFIG_DEBUG_COMMAND_SUPPORT = False
CONFIG_DIAG_CDC_USB_ETHERNET_FEATURE = 0
CONFIG_DIAG_CDC_USB_SERIAL_FEATURE = 0
CONFIG_DIAG_IPMI_FEATURE = 0
CONFIG_MICRO_SERVER_BOARD_REVISION = 0
CONFIG_SWITCH_BOARD_REVISION = 1
CONFIG_DIAG_FUNCTION_TEST = 1

# Parameters
DIAG_FOR_ONIE = False

DIAG_DEFAULT_SWITCH_BOARD_TYPE_FILE = \
    "/usr/local/accton/parameter/switch_board_type"
DIAG_DEFAULT_INFORMATION_FILE = "/tmp/.accton_diag_test_message.txt"
# DIAG_DEFAULT_INFORMATION_FILE_1 = "/tmp/.accton_diag_test_message1.txt"
DIAG_DEFAULT_MAXIMUM_POWER_CYCLE_FILE = \
        "/usr/local/accton/parameter/maximum_power_cycle_count"
DIAG_DEFAULT_POWER_CYCLE_FILE = \
  "/usr/local/accton/parameter/power_cycle_count"
DIAG_DEFAULT_POWER_CYCLE_DUMMY_FILE =\
        "/tmp/.accton_power_cycle_dummy_file.txt"
DIAG_DEFAULT_POWER_CYCLE_AVOTON_PASSED_COUNT_FILE =\
        "/usr/local/accton/parameter/power_cycle_avoton_passed_count"
DIAG_DEFAULT_POWER_CYCLE_AVOTON_FAILED_COUNT_FILE =\
        "/usr/local/accton/parameter/power_cycle_avoton_failed_count"
DIAG_DEFAULT_POWER_CYCLE_BMC_PASSED_COUNT_FILE =\
        "/usr/local/accton/parameter/power_cycle_bmc_passed_count"
DIAG_DEFAULT_POWER_CYCLE_BMC_FAILED_COUNT_FILE =\
        "/usr/local/accton/parameter/power_cycle_bmc_failed_count"

DIAG_DEFAULT_US_CARD_NUMBER_FILE = "/usr/local/accton/parameter/us_card_number"

# define DIAG_DEFAULT_SWITCH_BOARD_TYPE_FILE = \
#   "/usr/local/accton/parameter/switch_board_type"
DIAG_DEFAULT_MAXIMUM_COLD_START_SYSTEM_COUNT_FILE = \
    "/usr/local/accton/parameter/maximum_cold_start_system_count"
DIAG_DEFAULT_COLD_START_SYSTEM_COUNT_FILE = \
    "/usr/local/accton/parameter/cold_start_system_count"
DIAG_DEFAULT_COLD_START_SYSTEM_PASSED_COUNT_FILE = \
    "/usr/local/accton/parameter/cold_start_system_passed_count"
DIAG_DEFAULT_COLD_START_SYSTEM_FAILED_COUNT_FILE = \
    "/usr/local/accton/parameter/cold_start_system_failed_count"
DIAG_DEFAULT_MAXIMUM_HW_POWER_OFF_COUNT_FILE = \
    "/usr/local/accton/parameter/maximum_hw_power_off_count"
DIAG_DEFAULT_HW_POWER_OFF_COUNT_FILE = \
    "/usr/local/accton/parameter/diag_hw_power_off_count"
DIAG_DEFAULT_DIAGNOSTIC_TEST_COUNT_FILE = \
    "/usr/local/accton/parameter/diag_test_count"
DIAG_IS_PSU21_PLUGGED_FILE = \
    "/usr/local/accton/parameter/is_psu21_plugged"
DIAG_IS_DELTA_PSU_PLUGGED_FILE = \
    "/usr/local/accton/parameter/is_delta_psu_plugged"
DIAG_IS_CPLD_RESET_ENABLED_FILE = \
    "/usr/local/accton/parameter/is_cpld_reset_enabled"
if DIAG_FOR_ONIE:
    DIAG_DEFAULT_DIAGNOSTIC_TEST_LOG_FILE = \
    "/mnt/disk/diag/log/diag_main-10200.log"
else:
    DIAG_DEFAULT_DIAGNOSTIC_TEST_LOG_FILE = \
    "/usr/local/accton/log/diag_main-10200.log"
DIAG_IS_MCP2221A_USED_FILE = \
    "/usr/local/accton/parameter/is_mcp2221a_used"
DIAG_BMC_PROMPT = \
    "/usr/local/accton/parameter/bmc_prompt"

DIAG_IMAGE_AUTO_UPGRADE = \
    "/usr/local/accton/parameter/image_auto_upgrade"
DIAG_BIOS_VERSION = \
    "/usr/local/accton/parameter/bios_version"
DIAG_BIOS_FILE_NAME = \
    "/usr/local/accton/parameter/bios_file_name"

DIAG_IOB_VERSION = \
    "/usr/local/accton/parameter/iob_version"
DIAG_IOB_FILE_NAME = \
    "/usr/local/accton/parameter/iob_file_name"

DIAG_16Q_DOM_VERSION = \
    "/usr/local/accton/parameter/16q_dom_version"
DIAG_16Q_DOM_FILE_NAME = \
    "/usr/local/accton/parameter/16q_dom_file_name"

DIAG_16O_DOM_VERSION = \
    "/usr/local/accton/parameter/16o_dom_version"
DIAG_16O_DOM_FILE_NAME = \
    "/usr/local/accton/parameter/16o_dom_file_name"

DIAG_4DD_DOM_VERSION = \
    "/usr/local/accton/parameter/4dd_dom_version"
DIAG_4DD_DOM_FILE_NAME = \
    "/usr/local/accton/parameter/4dd_dom_file_name"

DIAG_TH3_VERSION = \
    "/usr/local/accton/parameter/th3_version"
DIAG_TH3_FILE_NAME = \
    "/usr/local/accton/parameter/th3_file_name"

DIAG_16Q_PHY_EE_VERSION = \
    "/usr/local/accton/parameter/16q_phy_ee_version"
DIAG_16Q_PHY_EE_FILE_NAME = \
    "/usr/local/accton/parameter/16q_phy_ee_file_name"

DIAG_16O_PHY_EE_VERSION = \
    "/usr/local/accton/parameter/16o_phy_ee_version"
DIAG_16O_PHY_EE_FILE_NAME = \
    "/usr/local/accton/parameter/16o_phy_ee_file_name"

DIAG_4DD_PHY_EE_VERSION = \
    "/usr/local/accton/parameter/4dd_phy_ee_version"
DIAG_4DD_PHY_EE_FILE_NAME = \
    "/usr/local/accton/parameter/4dd_phy_ee_file_name"

DIAG_BCM5396_VERSION = \
    "/usr/local/accton/parameter/bcm5396_version"
DIAG_BCM5396_FILE_NAME = \
    "/usr/local/accton/parameter/bcm5396_file_name"

DIAG_PIM_MUX_CPLD_FILE_NAME = \
    "/usr/local/accton/parameter/pim_mux_cpld_file_name"
DIAG_PIM16O_MUX_CPLD_FILE_NAME = \
    "/usr/local/accton/parameter/pim16o_mux_cpld_file_name"
DIAG_SMB_CPLD_USER_CODE_FILE_NAME = \
    "/usr/local/accton/parameter/smb_cpld_user_code_file_name"
DIAG_SCM_CPLD_USER_CODE_FILE_NAME = \
    "/usr/local/accton/parameter/scm_cpld_user_code_file_name"
DIAG_FCM_T_CPLD_USER_CODE_FILE_NAME = \
    "/usr/local/accton/parameter/fcm_t_cpld_user_code_file_name"
DIAG_FCM_B_CPLD_USER_CODE_FILE_NAME = \
    "/usr/local/accton/parameter/fcm_b_cpld_user_code_file_name"
DIAG_PDB_CPLD_USER_CODE_FILE_NAME = \
    "/usr/local/accton/parameter/pdb_cpld_user_code_file_name"
DIAG_FAN_VENDOR_NAME = \
    "/usr/local/accton/parameter/fan_vendor_name"
DIAG_RW_FRU_SPEED_UP = \
    "/usr/local/accton/parameter/rw_fru_speed_up"

DIAG_FPGA_MODEL = \
    "/usr/local/accton/parameter/diag_fpga_model"
DIAG_BI_MODE_FLAG = \
    "/usr/local/accton/parameter/burning_mode_flag"
BMC_CURRENT_VERSION_FILE = \
    "/usr/local/accton/parameter/bmc_current_version"

DIAG_ITEM143_TEST_COUNT_FILE = \
    "/usr/local/accton/parameter/diag_item_143_test_count"
DIAG_ITEM144_TEST_COUNT_FILE = \
    "/usr/local/accton/parameter/diag_item_144_test_count"
DIAG_ITEM145_TEST_COUNT_FILE = \
    "/usr/local/accton/parameter/diag_item_145_test_count"
DIAG_ITEM146_TEST_COUNT_FILE = \
    "/usr/local/accton/parameter/diag_item_146_test_count"
DIAG_ITEM147_TEST_COUNT_FILE = \
    "/usr/local/accton/parameter/diag_item_147_test_count"

DIAG_RUN_STRESS_MODE = \
   "/usr/local/accton/parameter/diag_run_stress_mode"

# DIAG_DEFAULT_MCELOG_TEST_LGG_FILE = \
#   "/var/log/mcelog"

# DIAG_BI_MODE = int(my_check_output("cat %s" % DIAG_BI_MODE_FLAG).strip())
# = = = = = = = = = Set by Anber = = = = = = = = =
DIAG_BI_MODE = 1
# = = = = = = = = = = = = = = =  = = = = = = = = =
revision_string = ['R0A', 'R0B', 'R0C', 'R01']
micro_server_name = \
    "Quanta Micro Server Board Rev " +  \
    revision_string[CONFIG_MICRO_SERVER_BOARD_REVISION]
switch_revision_name = \
    "Minipack Board Rev " + revision_string[CONFIG_SWITCH_BOARD_REVISION]

diag_switch_board_type = 0


# BMC definitions
IPMITOOL_DEFAULT_INFORMATION_FILE = "/tmp/.accton_bmc_test_message.txt"
MAXIMUM_BUFFER_LENGTH = 512
MAXIMUM_STRING_LENGTH = MAXIMUM_BUFFER_LENGTH-1
MAXIMUM_TTY_BUFFER_LENGTH = 512
MAXIMUM_TTY_STRING_LENGTH = MAXIMUM_TTY_BUFFER_LENGTH-1
MAXIMUM_FAN_NUMBER = 8

MINIMUM_MICRO_SERVER_CARD_NUMBER = 1
MAXIMUM_MICRO_SERVER_CARD_NUMBER = 12
MINIMUM_MICRO_SERVER_CARD_NUMBER_PER_BOARD = 1
MAXIMUM_MICRO_SERVER_CARD_NUMBER_PER_BOARD = 2
MINIMUM_BMC_CHIPSET_NUMBER = 1
MAXIMUM_BMC_CHIPSET_NUMBER = 12
MINIMUM_LEFT_LINE_CARD_SLOT_ID = 0
MAXIMUM_LEFT_LINE_CARD_SLOT_ID = 3
MINIMUM_RIGHT_LINE_CARD_SLOT_ID = 8
MAXIMUM_RIGHT_LINE_CARD_SLOT_ID = 11

BMC_LOGIN_PROMPT = "bmc login:"
BMC_PROMPT = "root@"
BMC_ROOT_PASSWORD = "0penBmc\n"
TTY_DEVICE_ACCESS_SLEEP_TIME_MS = 50
BMC_STANDARD_DELAY_MS = 100
BMC_SYSTEM_BOOT_UP_TIME = 165
BMC_WATCHDOG_TRIGGER_TIME = 30
TTY_DEVICE_ACCESS_WAITING_TIME_MS = 200
MAXIMUM_TEST_RETRY = 3
MAXIMUM_TTY_RETRY = 3
TTY_RETRY_DELAY_SECOND = 1
MAXIMUM_CP2112_RETRY = 3
CP2112_RETRY_DELAY_SECOND = 1
MAXIMUX_I2C_READ_RETRY = 3
I2C_READ_RETRY_DELAY_SECOND = 1
MAXIMUM_PSU_READ_RETRY = 3
PSU_RETRY_DELAY_SECOND = 1
DIMM_TEMP_MAX = 66000
DIMM_TEMP_MIN = 11000

DIAG_STATUS_SUCCESS = 0
DIAG_STATUS_FAILED = -1
DIAG_STATUS_FAILURE = -1
DIAG_ERROR_EXPECTION = -5
DIAG_ERROR_FAN_FAILED = -7
DIAG_ERROR_TTY_OPEN = -11
DIAG_ERROR_TTY_WRITE = -12
DIAG_ERROR_TTY_READ = -13
DIAG_ERROR_TTY_WAIT = -14
DIAG_ERROR_SET_FAN_SPEED = -15

if DIAG_BI_MODE == 1:
    DIAG_DEFAULT_FAN_SPEED = 40
else:
    DIAG_DEFAULT_FAN_SPEED = 50

BMC_I2C_WAITING_TIME_MS = 2000
TTY_PROMPT_TIME_MS = 5000

W25Q128_SIZE = 16777216
W25Q32_SIZE = 4194304
M95M02_SIZE = 262144
BCM5396_SIZE = 128

DOM_FLASH_STR_16Q = '\"W25Q32.V\"'
DOM_FLASH_STR_16O = '\"MX25U3235E/F\"'
DOM_FLASH_STR_4DD = '\"W25Q32.V\"'

FRU_TYPE_NONE = 0   # not detected
FRU_TYPE_PIM_16Q = 1
FRU_TYPE_PIM_4DD = 2
FRU_TYPE_PIM_16O = 3
FRU_TYPE_UNKOWN = 4

PIM_TYPE_TO_NAME = {
    FRU_TYPE_PIM_16Q: "16Q",
    FRU_TYPE_PIM_4DD: "4DD",
    FRU_TYPE_PIM_16O: "16O",
}

FPGA_MODEL_ACCTON = 'ACCTON'
FPGA_MODEL_FACEBOOK = 'FACEBOOK'

BOARD_SMB   = 1 << 0
BOARD_SCM   = 1 << 1
BOARD_FCM_B = 1 << 2
BOARD_FCM_T = 1 << 3

BOARD_PDB_L = 1 << 4
BOARD_PDB_R = 1 << 5

BOARD_SIM   = 1 << 6
BOARD_PT    = 1 << 7 # special config, need to substract

BOARD_PSU_1 = 1 << 8
BOARD_PSU_2 = 1 << 9
BOARD_PSU_3 = 1 << 10
BOARD_PSU_4 = 1 << 11

BOARD_PIM_1 = 1 << 12
BOARD_PIM_2 = 1 << 13
BOARD_PIM_3 = 1 << 14
BOARD_PIM_4 = 1 << 15
BOARD_PIM_5 = 1 << 16
BOARD_PIM_6 = 1 << 17
BOARD_PIM_7 = 1 << 18
BOARD_PIM_8 = 1 << 19

BOARD_FAN_1 = 1 << 20
BOARD_FAN_2 = 1 << 21
BOARD_FAN_3 = 1 << 22
BOARD_FAN_4 = 1 << 23
BOARD_FAN_5 = 1 << 24
BOARD_FAN_6 = 1 << 25
BOARD_FAN_7 = 1 << 26
BOARD_FAN_8 = 1 << 27

BOARD_BSM   = 1 << 28

BOARD_FCM_ALL = BOARD_FCM_B | BOARD_FCM_T
BOARD_PDB_ALL = BOARD_PDB_L | BOARD_PDB_R
BOARD_PSU_ALL = BOARD_PSU_1 | BOARD_PSU_2 | BOARD_PSU_3 | BOARD_PSU_4
BOARD_PIM_ALL = BOARD_PIM_1 | BOARD_PIM_2 | BOARD_PIM_3 | BOARD_PIM_4 |\
                BOARD_PIM_5 | BOARD_PIM_6 | BOARD_PIM_7 | BOARD_PIM_8
BOARD_FAN_ALL = BOARD_FAN_1 | BOARD_FAN_2 | BOARD_FAN_3 | BOARD_FAN_4 |\
                BOARD_FAN_5 | BOARD_FAN_6 | BOARD_FAN_7 | BOARD_FAN_8

# do not include BOARD_PT in a whole chassis test
BOARD_ALL = (BOARD_SMB | BOARD_SCM | BOARD_SIM | BOARD_FCM_ALL |\
            BOARD_PDB_ALL | BOARD_PSU_ALL | BOARD_PIM_ALL |\
            BOARD_FAN_ALL | BOARD_BSM)

PIM_NUM_TO_ID = {
    1:BOARD_PIM_1, 2:BOARD_PIM_2, 3:BOARD_PIM_3, 4:BOARD_PIM_4,
    5:BOARD_PIM_5, 6:BOARD_PIM_6, 7:BOARD_PIM_7, 8:BOARD_PIM_8,
}

PIM_ID_TO_NUM = {
    BOARD_PIM_1:1, BOARD_PIM_2:2, BOARD_PIM_3:3, BOARD_PIM_4:4,
    BOARD_PIM_5:5, BOARD_PIM_6:6, BOARD_PIM_7:7, BOARD_PIM_8:8,
}

PSU_NUM_TO_ID = {
    1:BOARD_PSU_1, 2:BOARD_PSU_2, 3:BOARD_PSU_3, 4:BOARD_PSU_4,
}

PSU_ID_TO_NUM = {
    BOARD_PSU_1:1, BOARD_PSU_2:2, BOARD_PSU_3:3, BOARD_PSU_4:4,
}

FAN_NUM_TO_ID = {
    1:BOARD_FAN_1, 2:BOARD_FAN_2, 3:BOARD_FAN_3, 4:BOARD_FAN_4,
    5:BOARD_FAN_5, 6:BOARD_FAN_6, 7:BOARD_FAN_7, 8:BOARD_FAN_8,
}

BOARD_CONFIG_FILE = \
    "/usr/local/accton/parameter/board_config"

BOARD_CONFIG_MAP = {
    BOARD_ALL: ['ALL'],
    BOARD_PT: ['PT'],
    BOARD_SMB: ['SMB'],
    BOARD_SCM: ['SCM'],
    BOARD_SIM: ['SIM'],
    BOARD_BSM: ['BSM'],

    BOARD_FCM_ALL: ['FCM', 'FCM-ALL'],
    BOARD_FCM_B: ['FCM-B'],
    BOARD_FCM_T: ['FCM-T'],

    BOARD_PDB_ALL: ['PDB', 'PDB-ALL'],
    BOARD_PDB_L: ['PDB-L'],
    BOARD_PDB_R: ['PDB-R'],

    BOARD_PIM_ALL: ['PIM', 'PIM-ALL'],
    BOARD_PIM_1: ['PIM-1', 'PIM1'],
    BOARD_PIM_2: ['PIM-2', 'PIM2'],
    BOARD_PIM_3: ['PIM-3', 'PIM3'],
    BOARD_PIM_4: ['PIM-4', 'PIM4'],
    BOARD_PIM_5: ['PIM-5', 'PIM5'],
    BOARD_PIM_6: ['PIM-6', 'PIM6'],
    BOARD_PIM_7: ['PIM-7', 'PIM7'],
    BOARD_PIM_8: ['PIM-8', 'PIM8'],

    BOARD_PSU_ALL: ['PSU', 'PSU-ALL'],
    BOARD_PSU_1: ['PSU-1', 'PSU1'],
    BOARD_PSU_2: ['PSU-2', 'PSU2'],
    BOARD_PSU_3: ['PSU-3', 'PSU3'],
    BOARD_PSU_4: ['PSU-4', 'PSU4'],

    BOARD_FAN_ALL: ['FAN', 'FAN-ALL'],
    BOARD_FAN_1: ['FAN-1', 'FAN1'],
    BOARD_FAN_2: ['FAN-2', 'FAN2'],
    BOARD_FAN_3: ['FAN-3', 'FAN3'],
    BOARD_FAN_4: ['FAN-4', 'FAN4'],
    BOARD_FAN_5: ['FAN-5', 'FAN5'],
    BOARD_FAN_6: ['FAN-6', 'FAN6'],
    BOARD_FAN_7: ['FAN-7', 'FAN7'],
    BOARD_FAN_8: ['FAN-8', 'FAN8'],
}

BOARD_ID_REVISION = {
    0: "EVTB",
    1: "DVTA",
    2: "DVTB",
    3: "PVT",
    4: "EVTA",
    5: "MP",
    6: "BSM",
    7: "NOT DEFINED",
}