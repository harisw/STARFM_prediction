import numpy as np

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
	classified_pixel = np.zeros([1199, 1199], dtype=float)
	while(row<1197):
		col = 0
		while(col < 1197):
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
	center_pixel = np.empty([1199, 1199], dtype=float)
	while(row<1199):
		col = 0
		while(col<1199):
			window_sum = 0
			for i in range(0,2):
				for l in range(0,2):
					window_sum += float(images[row+i][col+l])
			new_pixel = window_sum/9
			center_pixel[row][col] = new_pixel
			col += 1
		row += 1
	return np.array(center_pixel)

# def thresholding(images, center_pixel):
# 	row = 0
# 	while(row<1197):
# 		col = 0
# 		while(col < 1197):
# 			threshold_pixel = center_pixel[row][col]
# 			for i in range(0,2):
# 				for l in range(0, 2):
# 					if float(images[row+i][col+l]) < center_pixel[row][col]:
# 						images[row+i][col+l] = 0
# 					else:
# 						images[row+i][col+l] = center_pixel[row][col]
# 			col += 1
# 		row += 1
# 	return images

# if __name__ == '__main__':
# 	parseInputPixel("L7SR.05-24-01.txt")
# # 	