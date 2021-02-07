#!/usr/bin/python

import sys
from os import listdir
from os.path import join

import cli_ui
from glade_ui import GUI

# Dir where all system hwmon symlinks are located
HWMON_PATH = '/sys/class/hwmon'

# List of supported chips by name in hwmonX/name
SUPPORTED_CHIPS = ('nct6795')

from chip_sysfs_attributes import NCT6775

def get_nct_path():
	# Get all hwmon symlink in this dir
	for i in listdir(HWMON_PATH):
		# Open name file for hwmon dir
		with open(join(HWMON_PATH, i, 'name')) as f:
			# Return first element if exist and matches with supported chips
			for item in f.read().splitlines():
				if item in SUPPORTED_CHIPS:
					# Return full path to hwmon dir corresponding to chip
					return join(HWMON_PATH, i)


if __name__ == '__main__':
	path = get_nct_path()
	chip = NCT6775(path)

	gtk_debug = False

	if '--gtk' in sys.argv or gtk_debug:
		gui = GUI(chip)

	else:
		ui = cli_ui.Cli_UI(chip)
		ui.cli_ui()

