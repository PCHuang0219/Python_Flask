import sys
sys.path.append("..")
from lib import settings
settings.init()
from lib.utils import printException
import subprocess

# Generate lib/settings.py Class DUT
p = subprocess.call(['python3','Config/getAllConfig.py'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# Print the terminal output to stdout as well as writing to log file.
settings.glb.setVerbosity('high')

# Import the test script
from Facebook.fpga_IOB_0002 import FPGA_IOB_0002

# Initialize and run script.
# Select DUT1 as the test device.
dut1 = settings.Minipack_COMe()

tc_1 = FPGA_IOB_0002(dut1,"test")
#tc_1.init()
tc_1.run()
tc_1.terminate()