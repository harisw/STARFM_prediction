import numpy as np
import central_filter
from math import sqrt
from tqdm import tqdm

noise_const = 0.005

def compute_diff(first_img, second_img):
	diff_pixel = np.zeros([1199, 1199], dtype=float)
	row = 0
	while(row < 1199):
		col = 0
		while(col < 1199):
			diff_pixel[row][col] = abs(float(first_img[row][col]) - float(second_img[row][col]))
			col += 1
		row += 1
	return np.array(diff_pixel)

def compute_distance(candidate_pixel, central_pixel):
	row = 0
	dist_pixel = np.zeros([1199, 1199], dtype=float)
	bar = tqdm(total=1199)
	print "Computing distance\n"

	while(row<1197):
		col = 0
		while(col < 1197):
			threshold_pixel = central_pixel[row][col]
			for i in range(0,2):
				for l in range(0, 2):
					pos_y = row+i
					pos_x = col+l
					if pos_x == 1 and pos_y == 1:
						continue									#KALO DI TENGAH
					elif float(candidate_pixel[pos_y][pos_x]) == central_pixel[row][col]:	#KALO NILAINYA SAMA DENGAN CENTRAL PIXEL
						if (i == 0 or i == 2) and (l == 0 or l == 2):
							dist_pixel[pos_y][pos_x] = sqrt(2)		#KALO DI POJOK SEARCH WINDOW
						else:
							dist_pixel[pos_y][pos_x] = 1			#KALO DI KIRI/KANAN/ATAS/BAWAH
					# print dist_pixel[pos_y][pos_x]
			col += 1
		bar.update(1)
		row += 1
	bar.close()
	# print(dist_pixel)
	return dist_pixel

def compute_combined_weight(spec_diff, temp_diff, dist_pixel):
	combined_pixel = np.ones([1199, 1199], dtype=float)
	row = 0
	while(row<1199):
		col = 0
		while(col < 1199):
			combined_pixel[row][col] = spec_diff[row][col] * temp_diff[row][col] * dist_pixel[row][col]
			#Compute C[ijk]
			col += 1
		row += 1

	combined_sum = np.sum(combined_pixel)
	weight_pixel = np.ones([1199, 1199], dtype=float)
	row = 0
	print combined_sum
	while(row < 1199):
		col = 0
		while(col < 1199):
			if combined_pixel[row][col] != 0:
				weight_pixel[row][col] = (1 / combined_pixel[row][col]) / (1 / combined_sum)
			col += 1
		row += 1
	return weight_pixel

def refine_pixel(candidate_pixel, spec_diff, temp_diff):
	spec_max = spec_diff.max()
	temp_max = temp_diff.max()
	row = 0
	while(row<1199):
		col = 0
		while(col < 1199):
			if candidate_pixel[row][col] > (spec_max + noise_const) and candidate_pixel[row][col] > (temp_max + noise_const):
				candidate_pixel[row][col] = 0
			col += 1
		row += 1
	return candidate_pixel

def generate_prediction(Lk, Mk, M0, weight):
	pixel_result = np.empty([1199, 1199], dtype=float)
	row = 0
	# bar = IncrementalBar('Processing', max=1199)
	print "Generating Prediction Pixel\n"
	while(row<1199):
		col = 0
		while(col < 1199):
			pixel_result[row][col] = weight[row][col] * (float(M0[row][col]) + float(Lk[row][col]) - float(Mk[row][col]))
			col += 1
		# bar.next()
		row += 1
	# bar.finish()
	return pixel_result

if __name__ == '__main__':
	Lkimg = central_filter.parseInputPixel("L7SR.05-24-01.txt")
	Mkimg = central_filter.parseInputPixel("MOD09GHK.05-24-01.green.txt")
	M0img = central_filter.parseInputPixel("MOD09GHK.06-04-01.green.txt")
	
	central_pixel = central_filter.getCentralPixel(Lkimg)
	classified_pixel = central_filter.unsupervisedClassification(Lkimg, central_pixel)

	spec_diff = compute_diff(Lkimg, Mkimg)
	temporal_diff = compute_diff(Mkimg, M0img)
	dist_pixel = compute_distance(classified_pixel, central_pixel)
	
	combined_pixel = compute_combined_weight(spec_diff, temporal_diff, dist_pixel)
	candidate_pixel = refine_pixel(classified_pixel, spec_diff, temporal_diff)
	
	weight_pixel = compute_combined_weight(spec_diff, temporal_diff, dist_pixel)

	pixel_result = generate_prediction(Lkimg, Mkimg, M0img, weight_pixel)
	print pixel_result