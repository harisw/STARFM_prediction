import numpy as np
import central_filter
import write as w
from math import sqrt
from tqdm import tqdm
noise_const = 0.005

<<<<<<< HEAD
pixel_dimension = 1124
central_pixel_dimension = pixel_dimension - 2

Lkpixel = "WV_red_1812.txt"
Mkpixel = "L8_red_0701.txt"
M0pixel = "L8_red_0411.txt"	

=======
pixel_dimension = 1125
central_pixel_dimension = pixel_dimension - 2

>>>>>>> 74781847ea95082fa74580ec01b5e12c999ae5fe
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

<<<<<<< HEAD
def refinePixel(candidate_pixel, pixel_diff):
	pixel_max = pixel_diff.max()
	row = 0
	refined_pixel = np.ones([pixel_dimension, pixel_dimension], dtype=float)
	while(row<pixel_dimension):
		col = 0
		while(col < pixel_dimension):
			if candidate_pixel[row][col] > (pixel_max + noise_const):
=======
def refinePixel(candidate_pixel, spec_diff, temp_diff):
	spec_max = spec_diff.max()
	temp_max = temp_diff.max()
	row = 0
	refined_pixel = np.ones([pixel_dimension, pixel_dimension], dtype=float)
	print("\nSpec Max "+str(spec_max))
	print("\nTemp Max "+str(temp_max))
	while(row<pixel_dimension):
		col = 0
		while(col < pixel_dimension):
			if candidate_pixel[row][col] > (spec_max + noise_const) and candidate_pixel[row][col] > (temp_max + noise_const):
>>>>>>> 74781847ea95082fa74580ec01b5e12c999ae5fe
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
<<<<<<< HEAD
	bar.close()
	return pixel_result

if __name__ == '__main__':
	Lkimg = central_filter.parseInputPixel(Lkpixel)
	Mkimg = central_filter.parseInputPixel(Mkpixel)
	M0img = central_filter.parseInputPixel(M0pixel)
=======
	bar.close()
	return pixel_result

def writePixel(pixel_result, target_file, pixel_type='regular'):
	print "Writing result to file\n"
	offset = len(pixel_result[0])
	bar = tqdm(total=offset)
	with open(target_file, 'w') as output_file:
		row = 0
		output_file.write(";\n")
		output_file.write("; ENVI ASCII Output of file: H:\ALLAH\WV FIX\WV_red_1812.dat [Mon May 21 13:46:05 2018]\n")
		output_file.write("; File Dimensions: 1125 samples x 1125 lines x 1 band\n")
		output_file.write("; Line Format    : (1125i7)\n")
		output_file.write(";\n")
		while(row<offset):
			col = 0
			one_row = "    "
			while(col < offset):
				if pixel_type == 'final':
					temp = pixel_result[row][col]
					temp = str(temp)
				else:
					temp = "{0:.2f}".format(pixel_result[row][col])
				one_row = one_row + temp + "    "
				col += 1
			row += 1
			bar.update(1)
			output_file.write(one_row)
			output_file.write("\n")
	bar.close()
	return

if __name__ == '__main__':
	# Pixel contoh
	# Lkimg = central_filter.parseInputPixel("L7SR.05-24-01.txt")
	# Mkimg = central_filter.parseInputPixel("MOD09GHK.05-24-01.green.txt")
	# M0img = central_filter.parseInputPixel("MOD09GHK.06-04-01.green.txt")

	# Pixel asli
	Lkimg = central_filter.parseInputPixel("WV_red_1812.txt")
	Mkimg = central_filter.parseInputPixel("L8_red_0701.txt")
	M0img = central_filter.parseInputPixel("L8_red_0411.txt")
>>>>>>> 74781847ea95082fa74580ec01b5e12c999ae5fe
	
	central_pixel = central_filter.getCentralPixel(Lkimg)
	classified_pixel = central_filter.unsupervisedClassification(Lkimg, central_pixel)
	spec_diff = computeDiff(Lkimg, Mkimg)
	temporal_diff = computeDiff(Mkimg, M0img)
	dist_pixel = computeDistance(classified_pixel, central_pixel)
	
<<<<<<< HEAD
	spec_candidate = spec_diff
	temporal_candidate = temporal_diff

	weight_pixel = computeCombinedWeight(spec_candidate, temporal_candidate, dist_pixel)
	pixel_result = generatePrediction(Lkimg, Mkimg, M0img, weight_pixel)
	# w.writePixel(pixel_result, 'result.txt')
	w.writePixelAsRow(pixel_result, 'row_result.txt')
=======
	candidate_pixel = refinePixel(classified_pixel, spec_diff, temporal_diff)
		
	weight_pixel = computeCombinedWeight(spec_diff, temporal_diff, dist_pixel)
	pixel_result = generatePrediction(Lkimg, Mkimg, M0img, weight_pixel)
	writePixel(pixel_result, 'result[target].txt', 'final')
>>>>>>> 74781847ea95082fa74580ec01b5e12c999ae5fe
