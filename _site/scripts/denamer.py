#!/usr/bin/env python3

import os
import readline

directory = input('\nPlease enter directory for images: ').strip()
ImageIDs = input('\nPlease enter Image IDs in a comma-separated list: \n\n').split(',')
print()
ext=['s','u']
tifs=[]
jpgs=[]

for filename in os.listdir(directory):
    if '.tif' in filename:
        tifs.append(filename)
    elif '.jpg' in filename:
        jpgs.append(filename)
    else: 
        print("{} is not a jpg or tif".format(filename))

correctly_denamed = 0
not_found = 0
not_found_list = []

for x in range(len(ImageIDs)):
    if len(tifs)>0:
        for i in ext:
            capture_seq = str(x+1) + str(i)+'.tif'
            image_id = str(ImageIDs[x].strip()) + str(i)+'.tif'
            if os.path.exists(directory+'/'+image_id):
                os.rename(directory+'/'+image_id, directory+'/'+capture_seq)
                print("{} denamed correctly to {}".format(image_id,capture_seq))
                correctly_denamed = correctly_denamed + 1
            elif os.path.exists(directory+'/'+capture_seq):
                print("{} already denamed".format(capture_seq))
            else:
                not_found = not_found + 1
                not_found_list.append(image_id)
                print("{} not found in folder".format(image_id))
    else:
        pass
    if len(jpgs)>0:
        for i in ext:
            capture_seq = str(x+1) + str(i)+'.jpg'
            image_id = str(ImageIDs[x].strip()) + str(i)+'.jpg'
            if os.path.exists(directory+'/'+image_id):
                os.rename(directory+'/'+image_id, directory+'/'+capture_seq)
                print("{} denamed correctly to {}".format(image_id,capture_seq))
            elif os.path.exists(directory+'/'+capture_seq):
                print("{} already denamed".format(capture_seq))
            else:
                print("{} not found in folder".format(image_id))
    else:
        pass

print("\n\nDenamer report: \n")
print("{} images correctly denamed".format(str(correctly_denamed)))

if not_found > 0:
    print("{} images not found in folder: ".format(str(not_found)))
print()
if not_found_list:
    ANSWER = input("Would you like to see the list of images not found in your folder? Y or N? ")
    if ANSWER == "Y" or ANSWER == "y":
        print("Images not found include the following: ")
        for i in not_found_list:
            print(i)
    else: 
        exit