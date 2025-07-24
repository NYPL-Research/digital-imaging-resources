#!/usr/bin/env python3

# dependencies:
# imagesize
# imagemagick
# joblib
# tqdm
# multiprocessing
# img2pdf


import os
import subprocess
import imagesize
import readline
import textwrap
# modules for parallel work
import multiprocessing
from joblib import Parallel, delayed
# provides a nice progress bar
import tqdm
# lossless PDF conversion
import img2pdf

intro_text = """This script will take a folder of tifs, jp2s, or jpgs as input and losslessly create a PDF in the
PDF_Storage folder on the server. The PDF will be created from jpgs sized to 3500px on the longest edge and
will create a new set of derivatives if not already available. If your tif files have already been moved to
RTG, this script can still create a PDF from the QC folder jpgs. However, you may want to drag the parent
folder named after your session instead of the QC folder because this will set the name of the PDF (even if
there are no tif files available). If your files have been renamed to Image IDs produced by MMS, you will
be prompted to provide a list of IDs copied from your work order to maintain proper image sequence."""

# Wrap this text.
list = textwrap.wrap(intro_text, width=75)

# Print each line.
print('\n')
for element in list:
    print(element)

server_folder = input("\nPlease drag in a folder to create a PDF from files and press [Enter]\n\n").rstrip()
QC_folder = os.path.join(server_folder,'QC')
PDF_name = server_folder.split('/')[-1]

def get_files(server_folder):
	# traverse root directory, and list directories as dirs and files as files
	big_file_list = []
	jpg_file_list = []
	for root, dirs, files in os.walk(server_folder):
		for file in files:
			if "s.tif" in file:
				make_jpgs = True
				big_file_list.append(os.path.join(root, file))
				if len(file) > 9:
					reorder = True
				else:
					reorder = False
			elif "j.jp2" in file:
				make_jpgs = True
				big_file_list.append(os.path.join(root, file))
				if len(file) > 9:
					reorder = True
				else:
					reorder = False			
			elif "s.jpg" in file:
				make_jpgs = False
				jpg_file_list.append(os.path.join(root, file))
				if len(file) > 9:
					reorder = True
				else:
					reorder = False
			elif "j.jpg" in file:
				make_jpgs = False
				jpg_file_list.append(os.path.join(root, file))
				if len(file) > 9:
					reorder = True
				else:
					reorder = False

	if jpg_file_list:
		return jpg_file_list, reorder, make_jpgs
	else:
		try:
			os.mkdir(QC_folder)
		except:
			pass
		return big_file_list, reorder, make_jpgs


def check_order(reorder, big_file_list):
	# preserve image order for non-sequentially named images
	if reorder:
			ImageIDs = input('\nPlease enter Image IDs in a comma-separated list and press [Enter] \n\n').split(', ')
			return ImageIDs
	else:
		return file_list

def get_img_dims(big_file_list):
	# check to see if images are primarily portrait or landscape oriented
	global dims
	width = 0
	height = 0
	for file in big_file_list:
		width, height = imagesize.get(file)
		if width > height:
			width = width + 1
		else:
			height = height + 1
	if height >= width:
		dims = 'x3500'
	else:
		dims = '3500x'



def create_jpg(i):
	# create jpg derivatives for lighter weight PDF
	cmd = 'convert {}[0] -quiet -resize {} -quality 100 {}.jpg'.format(os.path.join(server_folder,i), dims, os.path.join(QC_folder,os.path.basename(i[0:-4])))
	pro = subprocess.call(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 



def parallel_processing(big_file_list, make_jpgs, orientation):
	# run create_jpg in parallel, using all processing cores
	print('\nWorking...\n')
	if make_jpgs:
		num_cores = multiprocessing.cpu_count()
		Parallel(n_jobs=num_cores)(delayed(create_jpg)(file) for file in tqdm.tqdm(big_file_list))


def reorder(ImageIDs, reorder):
	# reorder file list according to image sequence on work order
	jpg_file_list = []
	for root, dirs, files in os.walk(server_folder):
		for file in files:
			if ".jpg" in file:
				if not "._" in file:
					jpg_file_list.append(os.path.join(root, file))

	if reorder:
		newfilelist = []
		paths = []
		for ID in ImageIDs:
			paths.append([x for x in jpg_file_list if ID.strip() in x])
		for path in paths:
			for pat in path:
				newfilelist.append(pat)
		return newfilelist
	else:
		jpg_file_list.sort(key=lambda x: int(os.path.basename(x).split('.')[-2]))
		return jpg_file_list


def create_pdf(jpg_file_list):
	# create PDF
	output_file = "/Volumes/ice/Public_Orders-Deliverables/{}.pdf".format(PDF_name)
	print("\nConverting image files into a PDF at {}\n".format(output_file))
	pdf_bytes = img2pdf.convert((jpg_file_list), first_frame_only=True)
	file = open(output_file,"wb")
	file.write(pdf_bytes)
	print('\nPDF created successfully\n')


def main():
	fileget = get_files(server_folder)
	ImageIDs = check_order(fileget[1], fileget[0])
	orientation = get_img_dims(fileget[0])
	parallel_processing(fileget[0],fileget[2], orientation)
	jpgfileget = reorder(ImageIDs, fileget[1])
	create_pdf(jpgfileget)

if __name__ == '__main__':
	main()
