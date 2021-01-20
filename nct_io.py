import os
from os import listdir
from os.path import isfile, join

def save_configuration(path_from, path_to):
	# Get all files in the hwmon dir
	files = [f for f in listdir(path_from) if isfile(join(path_from, f))]
	output = ''
	# 'key' is really file name
	# key-value pair used to match with load method
	for key in files:
		full_path = join(path_from, key)
		value = open(full_path).read()
		if value:
			output += '{}:{}'.format(key, value)
	out_file = open(path_to, 'w')
	out_file.write(output)


def load_configuration(path_from, path_to):
	# Load data from file and split to list 
	loaded_data = open(path_from, 'r').readlines()
	opened_files = []
	# Loop through the files to find all files possible to write before
	# writing and saving any file (atomic operation)
	for i in loaded_data:
		if i:
			key, value = i.split(':')
			try:
				# If file is writable, save opened file and value as tuple
				opened_files.append((open(join(path_to, key), 'w'), value))
			except PermissionError:
				pass

	# Loop through writable files along with values, write value to the
	# corresponding file
	for file, value in opened_files:
		file.write(value)