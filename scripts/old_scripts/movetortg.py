#!/usr/bin/env python3

import os
import subprocess
import tqdm
import re
import shutil

output_folder = input("\nPlease drag in the folder you would like to send to rtg and press [Enter]:\n\n").rstrip()
rtg_folder = '/Volumes/ice/rtg'
pants_folder = '/Volumes/ice/Traveling_Pants/Moved_to_RTG'


def check_for_spaces():
	if ' ' in output_folder:
		print('\nPlease remove spaces from your folder name and try again. Exiting.\n')
		exit()
	else:
		print('\nYour folder name is computer readable.\n')
		pass

def check_for_rename():

	renamelist = []
	for file in os.listdir(output_folder):
		if 'tif' in file:
			if not file.startswith('.'):
				if not re.search(r'^[\w-]{5,}(s|u).tif$', file):
					renamelist.append(file)
				
	if renamelist:
		for item in renamelist:
			print(item)
		print('\nPlease rename files listed above and try again.\n')
		exit()
	else:
		pass

def get_files():
	file_dict = {}
	file_dict[output_folder] = [file for file in os.listdir(output_folder) if re.search(r'^[\w-]{5,}(s|u).tif$', file)]

	return file_dict

def move_files(file_dict):

	for file in tqdm.tqdm(file_dict[output_folder]):
		# cmd = "rsync -W --remove-source-files '{}' '{}'".format(os.path.join(output_folder, file), rtg_folder)
		# pro = subprocess.Popen(cmd, bufsize=4096, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
		# 					stderr=subprocess.STDOUT)
		# pro.wait()
		pro = subprocess.call(["mv", os.path.join(output_folder, file), rtg_folder], stdin=None, stdout=None, stderr=None, shell=False)


def move_folder():

	shutil.move(output_folder, pants_folder)


def main():
	check_for_spaces()
	check_for_rename()
	fileget = get_files()
	move_files(fileget)
	move_folder()
	print()


if __name__ == '__main__':
	main()

