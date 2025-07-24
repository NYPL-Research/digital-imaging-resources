#!/usr/bin/env python3

import os
import readline
import subprocess
import multiprocessing
from joblib import Parallel, delayed
import tqdm

images= input('\nPlease drag your images to be rotated into the terminal window: \n\n').split()

def check_for_spaces():
    for x in images:
        if "\\" in x:
            print('\n\nUnable to rotate images. Check folder and hard drive names for spaces\n')
            exit()
        else:
            pass
    print('\nYour folder and hard drive names are computer readable\n')


def rotate_images(i):
    cmd = 'mogrify -quiet -rotate "-90" -type TrueColor {}'.format(i)
    pro = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 

def parallel_processing():
    print('Working...\n')
    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(rotate_images)(file) for file in tqdm.tqdm(images))

def main():
    check_for_spaces()
    parallel_processing()
    print()

if __name__ == '__main__':
    main()