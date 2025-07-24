#! /bin/bash
while true
do
	clear
	echo "==============================================================================="
	echo "- - - - - - - - - - - - - - - - Menu - - - - - - - - - - - - - - - - - - - - - "
	echo "==============================================================================="
	echo -e "\n" 
	echo " Enter 1 to rename images"
	echo " Enter 2 to dename images"
	echo " Enter 3 to rotate a selection of images 90 degrees to the left"
	echo " Enter 4 to rotate a selection of images 90 degrees to the right"
	echo " Enter 5 to rotate a selection of images 180 degrees"
	echo " Enter 6 to move a folder and all of its contents to the server or another HDD"
	echo " Enter 7 to move a folder and all of its contents to another DIU computer"
	echo " Enter 8 to merge two Capture One sessions"
	echo " Enter 9 to upload processed s and u files to the server"
	echo " Enter 10 to create a folder of jpg derivatives (3500px)"
	echo " Enter 11 to create a PDF from Tifs or Jpgs in PO-Deliverables on the server"
	echo " Enter 12 to convert work order 'Copy all Capture IDs' text to Image Get input"
	echo " Enter 13 to resequence a folder of images"
	echo " Enter 14 to move a folder of images on the server to RTG"
	echo " Enter 15 to create a random list of captures to repo check using command 16"
	echo " Enter 16 to download any available image from the repository"
	echo " Enter q to quit"
	echo -e "\n"
	echo -e "Enter your selection: \c"
	read answer
	case "$answer" in 
	1) /usr/local/bin/renamer.py ;;
	2) /usr/local/bin/denamer.py ;;
	3) /usr/local/bin/rotateleft.py ;;
	4) /usr/local/bin/rotateright.py ;;
	5) /usr/local/bin/rotateflip.py ;;
	6) /usr/local/bin/move.py ;;
	7) /usr/local/bin/transfer.py ;;
	8) /usr/local/bin/merge.py ;;
	9) /usr/local/bin/upload.py ;;
	10) /usr/local/bin/QC.py ;;
	11) /usr/local/bin/pdfmaker.py ;;
	12) /usr/local/bin/reporeplace.py ;;
	13) /usr/local/bin/sequencer.py ;;
	14) /usr/local/bin/movetortg.py ;;
	15) /usr/local/bin/repocall.py ;;
	16) /usr/local/bin/imageget.py ;;
	q) exit ;;
	esac
	echo -e "Enter return to continue /c"
	read input
done
