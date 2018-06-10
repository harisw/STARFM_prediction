import numpy as np

pixel_dimension = 1124
central_pixel_dimension = pixel_dimension - 2

def parseInputPixel(filename):
	images = []
	with open(filename) as f:
		temp = []
		temp = f.readlines()
		# print(temp)
	images = np.array(temp[5:])

	stripped_line = []
	for row in images:
		new_row = row.replace('    ', ' ')
		new_row = new_row.replace('   ', ' ')
		new_row = new_row.replace('  ', ' ')
		new_row = new_row.replace('\n', '')
		new_row = new_row.split(' ')
		if new_row[0] == '':
			new_row.pop(0)
		new_row = np.array(new_row)
		stripped_line.append(new_row)
	processed_img = np.array(stripped_line)
	# print processed_img[0][0]
	return processed_img
	# center_pixel = getCentralPixel(processed_img)
	# threshold_pixel = thresholding(processed_img, center_pixel)
	# print(threshold_pixel.shape)

def unsupervisedClassification(candidate_pixel, center_pixel):
	row = 0
	classified_pixel = np.zeros([pixel_dimension, pixel_dimension], dtype=float)
	while(row<central_pixel_dimension):
		col = 0
		while(col < central_pixel_dimension):
			threshold_pixel = center_pixel[row][col]
			for i in range(0,2):
				for l in range(0, 2):
					if float(candidate_pixel[row+i][col+l]) < center_pixel[row][col]:
						classified_pixel[row+i][col+l] = 0
					else:
						classified_pixel[row+i][col+l] = center_pixel[row][col]
			col += 1
		row += 1
	return classified_pixel
	
def getCentralPixel(images):
	row = 0
	center_pixel = np.empty([pixel_dimension, pixel_dimension], dtype=float)
	while(row<pixel_dimension):
		col = 0
		while(col<pixel_dimension):
			window_sum = 0
			for i in range(0,2):
				for l in range(0,2):
					window_sum += float(images[row+i][col+l])
			new_pixel = window_sum/9
			center_pixel[row][col] = new_pixel
			col += 1
		row += 1
	return np.array(center_pixel)