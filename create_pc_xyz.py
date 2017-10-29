import cv2
import numpy as np
import math
import sys
import os.path

MAX_ABS_DIST = 40000

output_filename = ''
if len(sys.argv) == 2:
	output_filename = os.path.splitext(os.path.basename(sys.argv[1]))[0] + '.xyz'
elif len(sys.argv) == 3:
	output_filename = sys.argv[2]
else:
	print("Invalid argument.")
	print("Usage: script.py depth.png")
	print("Usage: script.py depth.png out.xyz")
	sys.exit(1)

img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)

print('Converting {} to xyz format...'.format(sys.argv[1]))
print('Maximum dist: {}'.format(MAX_ABS_DIST))

v_angle = []
for i in range(0, 31 + 1):
	v_angle.append(math.radians(2.0) - math.radians(1 / 3) * i)

for i in range(0, 33 + 1):
	v_angle.append(math.radians(-8.53) - math.radians(1 / 2) * i)

point_num = 0
skip_x = 0
skip_y = 0
skip_z = 0
print('depth png size: {}'.format(img.shape[0] * img.shape[1]))
fd = open(output_filename, 'w')
for y in range(img.shape[0]):
	for x in range(img.shape[1]):
		dist = img[y,x]
		if dist == 0:
			continue
		point_num += 1
		A = dist * math.cos(v_angle[y])
		z_a = dist * math.sin(v_angle[y])
		h_angle = (math.pi * 1.5) - (math.pi * 2 / img.shape[1]) * x
		x_a = A * math.cos(h_angle)
		y_a = A * math.sin(h_angle)
		if abs(x_a) > MAX_ABS_DIST:
			skip_x += 1
			continue
		if abs(y_a) > MAX_ABS_DIST:
			skip_y += 1
			continue
		if abs(z_a) > MAX_ABS_DIST:
			skip_z += 1
			continue
		fd.write("%d %d %d\n" % (x_a, y_a, z_a))
fd.close()
print('Measured point num: {}'.format(point_num))
print("skip_x: {}".format(skip_x))
print("skip_y: {}".format(skip_y))
print("skip_z: {}".format(skip_z))
