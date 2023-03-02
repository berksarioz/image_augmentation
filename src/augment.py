'''
Author: Berk Sarioz
Date: Jan 10, 2022

Instructions:
Requires opencv installation for python.

Place this script in a sibling directory of 'data' (you can call it 'src')

You should be able to run the following command from the current directory of the script
and get your results at a sibling directory of 'data'.(tested on macOS environment)

python3 augment.py data/rgb data/normal data/depth --output augmentations_output --count 10
'''
import cv2
import numpy as np
import random
from os import mkdir, listdir
from os.path import isfile, join, isdir
import sys
 
user_args = sys.argv
i = 1 # skip first argument as it's the script file name
input_args = [] 

while (i < len(user_args)):
	if(user_args[i] not in ['--output', '--count']):
		input_args.append(user_args[i])
		i += 1
	else:
		if(user_args[i] == '--output'):
			output_arg = user_args[i+1]
			i += 2
		else: # it's the count argument
			modification_count_arg = int(user_args[i+1])
			i += 2


modification_array = []
while len(modification_array) < modification_count_arg:
	# resize
	resize_or_not = random.uniform(0, 1)
	if (resize_or_not < 0.7):
		resize_factor = 100 # do not resize 70% of the time
	else:
		resize_factor = random.randint(50, 150) # resize by 50%

	# rotate
	rotate_or_not = random.uniform(0, 1)
	if (rotate_or_not < 0.6):
		rotate_angle = 0 # do not rotate 60% of the time
	else:
		rotate_angle = random.randint(1, 359) # rotate from 1 to 359 degrees

	# grayscale
	grayscale_or_not = random.uniform(0, 1)
	if (grayscale_or_not < 0.8):
		grayscale_factor = False
	else:
		grayscale_factor = True

	# flip
	flip_or_not = random.uniform(0, 1)
	if (flip_or_not < 0.8):
		flip_factor = -1
	else:
		flip_factor = random.randint(0, 1)

	values = (resize_factor, rotate_angle, grayscale_factor, flip_factor)

	# Discard values if there is no modification to the original image
	# and make sure the modification isn't present in the list
	if (values != (100, 0, False, -1)) and (values not in modification_array):
		modification_array.append(values)

def resize_image(image, scale_percent):
	width = int(img.shape[1] * scale_percent / 100)
	height = int(img.shape[0] * scale_percent / 100)
	dim = (width, height)
	return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def grayscale_image(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# flip vertically with 0, horizontally with 1
def flip_image(image, num):
	return cv2.flip(image, num)


# account for user not entering / for the directory path
if (output_arg[-1] != '/'):
	output_arg += '/'
up_one_dir = '../'
output_dir = up_one_dir + output_arg

if(not isdir(output_dir)):
	mkdir(output_dir)

	for input_arg in input_args:
		# account for user not entering / for the directory path
		if (input_arg[-1] != '/'):
			input_arg += '/'
			input_dir = up_one_dir + input_arg


			files_arg = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
			filenames = [input_dir + f for f in files_arg]

			for filename in filenames:
				current_output_dir = output_dir + input_arg.split('/')[-2] + '-' + filename[-6:-4]
				mkdir(current_output_dir)
				for count, modification in enumerate(modification_array):
					img = cv2.imread(filename)
					# resize
					img = resize_image(img, modification[0])
					# rotate
					angle = modification[1]
					if (angle != 0):
						img = rotate_image(img, angle)
					# grayscale
					if(modification[2]):
						img = grayscale_image(img)
					# flip
					flip = modification[3]
					if(flip != -1):
						img = flip_image(img, flip)

					cv2.imwrite(current_output_dir + '/' + '{0:04}'.format(count) + '.png', img)

	print("\nImages modified with following values:\n")
	print("Resize_factor, Rotate_angle, Grayscale_factor, Flip_factor")
	for modification in modification_array:
		print(modification)
else:
	print('Output directory already exists.')
