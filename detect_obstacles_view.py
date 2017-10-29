import cv2
import numpy as np
import sys
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename', action="store")
parser.add_argument('-c', action='store', dest='dest_filename', help='Create an image file.', default=False)
options = parser.parse_args()

img = cv2.imread(options.filename, cv2.IMREAD_UNCHANGED)
img_dst = img.copy()

cascade_file = 'SPECIFY PATH TO CASCADE FILE'
cascade = cv2.CascadeClassifier(cascade_file)
if cascade.empty():
	print('Empty cascade file.')
	sys.exit(1)

cars = cascade.detectMultiScale(img_dst, 1.1, 3)
for (x, y, w, h) in cars:
        print(x, y, w, h)
        cv2.rectangle(img_dst, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

if options.dest_filename:
	print('writing {}'.format(options.dest_filename))
	cv2.imwrite(options.dest_filename, img_dst)
else:
	cv2.imshow('img_dst', img_dst)
	cv2.imshow('img', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
