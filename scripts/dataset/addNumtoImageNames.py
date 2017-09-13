#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
Purpose: This script is to add a specific number to image names in order to increment their number.
Functionality: In order to merge Test set and Training set together, Test set image names should be added with the highest number in the Training set.

Input: Train_DIR=Training set path, Test_DIR=Test set path,

Output: Together_DIR=Merged sets together path,

Usage: Python addNumtoImageNames.py --Train_DIR --Test_DIR --Together_DIR

Author: Seyed Majid Azimi
Date: 11th September 2017

Deutsches Zentrum für Luft und Raumfahrt e.V DLR

"""


import sys
import os
import argparse
import progressbar
from glob import glob
from skimage import io
import numpy as np
from termcolor import colored
#import subprocess


np.random.seed(5) # for reproducibility
progress = progressbar.ProgressBar(widgets=[progressbar.Bar('*', '[', ']'), progressbar.Percentage(), ' '])

"""
try:
    import cv2 
except ImportError:
    raise ImportError('Can\'t find OpenCV Python module. If you\'ve built it from sources without installation, '
                      'configure environemnt variable PYTHONPATH to "opencv_build_dir/lib" directory (with "python3" subdirectory if required)')
"""

def parse_args():
	"""Parse input arguments"""
	parser = argparse.ArgumentParser(description='addNumtoImageNames')
	
	parser.add_argument('--Train_DIR', dest='_trainDir', help='Path to Train set Directory',
		default='./train', type=str)

	parser.add_argument('--Test_DIR', dest='_testDir', help='Path to Test set Directory',
		default='./test', type=str)

	parser.add_argument('--Together_DIR', dest='_mergedDir', help='Path to Together set Directory',
		default='./together', type=str)

	args = parser.parse_args()

	return args


class Incrimentation(object):
	'''
	Read each image and its name. Add a specific number to each file name and save it.

	INPUT list 'inputpath': filepaths to all images of specific set
	INPUT list 'outputpath': filepaths to output images of specific set

	'''
    
	def __init__(self, inputpath, outputpath, number=55680):
		self.inputpath=inputpath
		self.outputpath=outputpath
		self.number=number
		print(colored(("\nInput Path is: {}".format(self.inputpath)), 'yellow'))
		self._ImagesNames = glob(self.inputpath+'/**') #/**/*more*  '/**/**'
		print(colored(self._ImagesNames, 'blue'))
		self.read(self._ImagesNames)


	def read(self, _ImagesNames):

		progress.currval = 0
		for image_idx in progress(range(len(self._ImagesNames))):
			#Incriment *imagePtr=image
			image = self.readImage(self._ImagesNames[image_idx])
			_IncImageName = self.incrementName(self._ImagesNames[image_idx],self.number)
			self.saveIncImage(image, _IncImageName, self.outputpath)

	def readImage(self, imagepath):
		'''
		Reading each image
	
		input: imagepath= path to image

		output: img= image file
		'''

		try:	
			print(colored(("\nimage path being read is : {}".format(imagepath)), 'green'))
			img = io.imread(imagepath)#plugin='simpleitk').astype(float)
	
		except Exception as e:
			raise("Can not read image")


		return img


	def incrementName(self, ImageName, number):
		'''
		Increment file name by an number
		>>> f = 'C:\\X\\Data\\foo.txt'
		>>> import os
		>>> os.path.basename(f)
		'foo.txt'
		>>> os.path.dirname(f)
		'C:\\X\\Data'
		>>> os.path.splitext(f)
		('C:\\X\\Data\\foo', '.txt')
		>>> os.path.splitext(os.path.basename(f))
		('foo', '.txt')

		or 
		>>> filename = "example.jpeg"
		>>> filename.split(".")[-1]
		'jpeg'

		No error when file doesn't have an extension:

		>>> "filename".split(".")[-1]
		'filename'

		But you must be careful:

		>>> "png".split(".")[-1]
		'png'    # But file doesn't have an extension


		head, tail = os.path.split("a/b/c/00001.dat")
		print(head,tail

		'''


		# split file base name from head of path file
		head, basename = os.path.split(ImageName)
		print("Head and Basename are: ", head, basename)
		
		# find out RGB category or grayscale
		category = os.path.split(head)[-1]

		#split file name from its format
		_fileName,_fileformat = os.path.splitext(basename)
		print("_fileName and _fileformat are: ", _fileName, _fileformat)

		#increment file name
		_incfileName = str(int(_fileName)+self.number)+_fileformat
		print("Incremented base Name is: ", _incfileName)

		#join paths all together
		if category=='RGB' or category=='grayscale':		
			_incfileName=os.path.join(c_incfileName)

		print("incremented full name is: ", _incfileName)


		return _incfileName


	def saveIncImage(self, image, _incfileName, _outpath):

		# append output directory path to incremented file path
		_fileName = os.path.join(_outpath,_incfileName)
		print(colored("\nSaving path is: {}".format(_fileName), 'red'))
		io.imsave(_fileName,image)
		#cv2.imwrite(outputpath+'/'+'{}'.format(_incfileName))

if __name__ == '__main__':
	args = parse_args()

	#_trainImages = glob(args._trainDir+'/**.jpg')#/**/*more*
	#_testImages = glob(args._testDir+'/**.jpg')#/**/*more*
	
	data = Incrimentation(args._testDir,args._mergedDir)
