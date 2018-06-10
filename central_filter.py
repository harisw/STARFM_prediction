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
	return processed_img

def unsupervisedClassification(candidate_pixel, center_pixel):
	row = 0
	classified_pixel = np.zeros([pixel_dimension, pixel_dimension], dtype=float)
	while(row<central_pixel_dimension):
		col = 0
		while(col < central_pixel_dimension):
			threshold_pixel = center_pixel[row][col]
			
			min_pixel = 1000000
			max_pixel = 0
			for i in range(0,3):
				for l in range(0, 3):
					# print min_pixel
					if int(candidate_pixel[row+i][col+l]) > max_pixel:
						max_pixel = int(candidate_pixel[row+i][col+l])	
					if int(candidate_pixel[row+i][col+l]) < min_pixel:
						min_pixel = int(candidate_pixel[row+i][col+l])

			threshold_point = (float(min_pixel) + float(max_pixel)) / 2.0
			for i in range(0,3):
				for l in range(0, 3):
					if float(candidate_pixel[row+i][col+l]) < threshold_point:
						classified_pixel[row+i][col+l] = 0
					else:
						classified_pixel[row+i][col+l] = center_pixel[row][col]
			col += 1
		row += 1
	return classified_pixel
	
def getCentralPixel(images):
	row = 0
	center_pixel = np.empty([pixel_dimension, pixel_dimension], dtype=float)
	while(row<central_pixel_dimension):
		col = 0
		while(col<central_pixel_dimension):
			window_sum = 0
			for i in range(0,3):
				for l in range(0,3):
					window_sum += int(images[row+i][col+l])
			new_pixel = float(window_sum)/9.0
			center_pixel[row][col] = new_pixel
			col += 1
		row += 1
	return np.array(center_pixel)