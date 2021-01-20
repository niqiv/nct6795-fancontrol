from os import listdir
from os.path import isfile, join
import re

from pwm import Pwm
import printtools as ppt
import cli_ui

# Hardcoded path for chip parameters
path = '/sys/devices/platform/nct6775.2592/hwmon/hwmon2/'

# Make list of all files in the directory
# This data can be saved to restore original settings later
files = [f for f in listdir(path) if isfile(join(path, f))]

pwm_fans = []

r = re.compile('^pwm[0-9]{1,2}$')

for i in filter(r.match, files):
	features = {
		f: int(open(path + f).read().strip('\n'))
		for f in files if i in f
		}
	#print(features)
	pwm = Pwm(i.lstrip('pwm'), path, features)
	pwm_fans.append(pwm)

ui = cli_ui.Cli_UI(pwm_fans)
ui.cli_ui()
