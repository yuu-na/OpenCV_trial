import cv2
import numpy as np
import sys
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', action='store', help='Filename for a normal image.')
parser.add_argument('-c', action='store', dest='dest_filename', help='Create an image file.', default=False)
parser.add_argument('-d', action='store', dest='depth_directory', help='Path for depth image directory.', default=False)
parser.add_argument('-g', action='store_true', dest='rg_normal', help='Use red and green for detection. (default is red only)', default=False)
options = parser.parse_args()

# Read a normal image.
img = cv2.imread(options.filename, cv2.IMREAD_UNCHANGED)
# Read a depth image corresponding to the normal image.
pic_number = options.filename[:options.filename.find('_')]
if options.depth_directory is False:
	depth_img = cv2.imread('../depth/' + pic_number + '_depth.png', cv2.IMREAD_UNCHANGED)
else:
	depth_img = cv2.imread(options.depth_directory + '/' + pic_number + '_depth.png', cv2.IMREAD_UNCHANGED)

# Consider normal colored green and red are obstacles.
BGR = cv2.split(img)
src_green = BGR[1]
src_red = BGR[2]

# Fill up black pixels
kernel = np.ones((3, 3), np.uint8)
green = cv2.dilate(src_green, kernel, iterations = 1)
red = cv2.dilate(src_red, kernel, iterations = 1)

# Make images binary pictures
THRESHOLD = 100
ret, obs_green = cv2.threshold(green, THRESHOLD, 255, cv2.THRESH_BINARY)
ret, obs_red = cv2.threshold(red, THRESHOLD, 255, cv2.THRESH_BINARY)
if options.rg_normal:
	print('use green and red for detection.')
	obs = cv2.bitwise_or(obs_green, obs_red)
else:
	print('use red for detection.')
	obs = obs_red

# Filter out unnecessary area
normal = cv2.bitwise_and(img, img, mask = obs)
depth = cv2.bitwise_and(depth_img, depth_img, mask = obs)

# Find countours
retval, depth_bw = cv2.threshold(np.ceil(depth / 256).astype('uint8'), 10, 255, cv2.THRESH_BINARY)
retimg, contours, hierarchy = cv2.findContours(depth_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# For showing result.
result_normal = img.copy()

# Draw rectangle for countours.
detect_count = 0
for i in range(0, len(contours)):
	# Remove noize and large rectangles
	if len(contours[i]) > 0:
		rect = contours[i]
		x, y, w, h = cv2.boundingRect(rect)
		if (w * h) < 200 or (w * h) > 10000:
			continue
		cv2.rectangle(result_normal, (x, y), (x + w, y + h), (0, 0, 255), 2)
		detect_count = detect_count + 1
print('detect_count: {}'.format(detect_count))

height, width = result_normal.shape[:2]
forward_view = result_normal[0:height - 1, int(width / 5 * 2):int(width / 5 * 3)]

if options.dest_filename:
	print('writing {}'.format(options.dest_filename))
	cv2.imwrite(options.dest_filename, result_normal)
else:
	cv2.imshow('obs', obs)
	cv2.imshow('normal', normal)
	cv2.imshow('depth bw', depth_bw)
	cv2.imshow('result normal', result_normal)
	cv2.imshow('forward', forward_view)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
