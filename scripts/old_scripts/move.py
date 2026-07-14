#!/usr/bin/env python3

import os
import stat
import subprocess
# modules for parallel work
from joblib import Parallel, delayed
# provides a nice progress bar


move_folder = input("\nPlease drag in the folder you would like to move and press [Enter]:\n\n").rstrip()
target_folder = input("\nPlease drag in the folder where you would like to move your files to and press [Enter]\n\n").rstrip()

def check_for_spaces():
	if ' ' in move_folder or ' ' in target_folder:
		print('Check folder and hard drive names for spaces')
		exit()
	else:
		print('\nYour folder and hard drive names are computer readable\n')
		pass

def set_folder_permissions():
	os.chmod(target_folder, 0o777)
	print('Your target folder permissions have been set to {} (0777 is most permissive)\n'.format(oct(stat.S_IMODE(os.lstat(target_folder).st_mode))))

def move_files():
	cmd = "rsync -ratvhP --progress '{}' '{}'".format(move_folder, target_folder)
	pro = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
						stderr=subprocess.STDOUT, preexec_fn=os.setsid)

	while pro.poll() is None:
		line = pro.stdout.readline()
		print(line)

def main():
	check_for_spaces()
	move_files()
	set_folder_permissions()

if __name__ == '__main__':
	main()


