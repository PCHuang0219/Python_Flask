import sys
sys.path.append("..")
from lib import settings
settings.init()
from lib.utils import printException
import subprocess

# Generate lib/settings.py Class DUT
p = subprocess.call(['python3','../Config/get_all_config.py'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# Print the terminal output to stdout as well as writing to log file.
settings.glb.setVerbosity('high')

argv_list = sys.argv

for i in range(1,len(argv_list)):
    locals()["argv%s"%i] = argv_list[i]

# Import the test script
from SONiC.sample_code import SONiC_sample
# Initialize and run script.
dut = settings.AS7816_64X()
testcase = SONiC_sample(dut, job_id='SONiC_test')
testcase.run()
testcase.stop()
