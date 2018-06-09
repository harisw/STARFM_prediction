import numpy as np
import central_filter
import write as w
from math import sqrt
from tqdm import tqdm
noise_const = 0.005

pixel_dimension = 1125
central_pixel_dimension = pixel_dimension - 2

Lkpixel = "WV_blue_1812.txt"
Mkpixel = "L8_blue_0701.txt"
M0pixel = "L8_blue_0411.txt"	

def computeDiff(first_img, second_img):
	diff_pixel = np.zeros([pixel_dimension, pixel_dimension], dtype=float)
	row = 0
	while(row < pixel_dimension):
		col = 0
		while(col < pixel_dimension):
			diff_pixel[row][col] = abs(float(first_img[row][col]) - float(second_img[row][col]))
			col += 1
		row += 1
	return np.array(diff_pixel)

def computeDistance(candidate_pixel, central_pixel):
	row = 0
	dist_pixel = np.zeros([pixel_dimension, pixel_dimension], dtype=float)
	bar = tqdm(total=pixel_dimension)
	print "Computing distance\n"
	while(row<central_pixel_dimension):
		col = 0
		while(col < central_pixel_dimension):
			threshold_pixel = central_pixel[row][col]
			for i in range(0,3):
				for l in range(0, 3):
					pos_y = row+i
					pos_x = col+l
					if pos_x == 1 and pos_y == 1:
						continue									#KALO DI TENGAH
					elif float(candidate_pixel[pos_y][pos_x]) == central_pixel[row][col]:	#KALO NILAINYA SAMA DENGAN CENTRAL PIXEL
						dist_pixel[pos_y][pos_x] = sqrt( (col - pos_x)**2 + (row - pos_y)**2)
			col += 1
		bar.update(1)
		row += 1
	bar.close()
	return dist_pixel

def computeCombinedWeight(spec_diff, temp_diff, dist_pixel):
	combined_pixel = np.ones([pixel_dimension, pixel_dimension], dtype=float)
	row = 0
	while(row<pixel_dimension):
		col = 0
		while(col < pixel_dimension):
			combined_pixel[row][col] = spec_diff[row][col] * temp_diff[row][col] * dist_pixel[row][col]
			#Compute C[ijk]
			col += 1
		row += 1
	combined_sum = np.sum(combined_pixel)
	weight_pixel = np.ones([pixel_dimension, pixel_dimension], dtype=float)
	row = 0
	print combined_sum
	while(row < pixel_dimension):
		col = 0
		while(col < pixel_dimension):
			if combined_pixel[row][col] != 0:
				weight_pixel[row][col] = (1 / combined_pixel[row][col]) / (1 / combined_sum)
			col += 1
		row += 1
	return weight_pixel

def refinePixel(candidate_pixel, pixel_diff):
	pixel_max = pixel_diff.max()
	row = 0
	refined_pixel = np.ones([pixel_dimension, pixel_dimension], dtype=float)
	while(row<pixel_dimension):
		col = 0
		while(col < pixel_dimension):
			if candidate_pixel[row][col] > (pixel_max + noise_const):
				refined_pixel[row][col] = 0
			else:
				refined_pixel[row][col] = candidate_pixel[row][col]
			col += 1
		row += 1
	return refined_pixel

def generatePrediction(Lk, Mk, M0, weight):
	pixel_result = np.empty([pixel_dimension, pixel_dimension], dtype=int)
	row = 0
	print('Computing Prediction pixel')
	bar = tqdm(total=pixel_dimension)
	while(row<pixel_dimension):
		col = 0
		while(col < pixel_dimension):
			pixel_result[row][col] = int(weight[row][col] * (float(M0[row][col]) + float(Lk[row][col]) - float(Mk[row][col])))
			col += 1
		bar.update(1)
		row += 1
	bar.close()
	return pixel_result

if __name__ == '__main__':
	Lkimg = central_filter.parseInputPixel(Lkpixel)
	Mkimg = central_filter.parseInputPixel(Mkpixel)
	M0img = central_filter.parseInputPixel(M0pixel)
	
	central_pixel = central_filter.getCentralPixel(Lkimg)
	classified_pixel = central_filter.unsupervisedClassification(Lkimg, central_pixel)
	spec_diff = computeDiff(Lkimg, Mkimg)
	temporal_diff = computeDiff(Mkimg, M0img)
	dist_pixel = computeDistance(classified_pixel, central_pixel)
	
	spec_candidate = spec_diff
	temporal_candidate = temporal_diff

	weight_pixel = computeCombinedWeight(spec_candidate, temporal_candidate, dist_pixel)
	pixel_result = generatePrediction(Lkimg, Mkimg, M0img, weight_pixel)
	w.writePixel(pixel_result, 'result.txt')