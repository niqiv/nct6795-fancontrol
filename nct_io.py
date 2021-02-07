import os
from os import listdir
from os.path import isfile, join

'''
Configuration can be saved and loaded.
Saving 
'''

def save_configuration(chip, path_to):
	with open(path_to, 'w+') as f:
		for controller in chip.pwm_controllers:
			for i in controller.attributes:
				if i.can_read() and i.can_write():
					f.write('{}:{}\n'.format(
						i, i.get_value())
					)

def load_configuration(chip, path_from):
	with open(path_from, 'r') as f:
		for line in f.read().split('\n'):
			if line:
				file, value = line.split(':')
				chip.set_value_in_file(file, value)