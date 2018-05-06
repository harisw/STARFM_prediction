import numpy as np
import central_filter
from math import sqrt

def compute_diff(first_img, second_img):
	diff_pixel = np.zeros([1199, 1199], dtype=float)
	row = 0
	print first_img[0][0]
	print second_img[0][0]
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
						print "Posisi Y nya ", pos_y," Posisi X nya ", pos_x
						if (i == 0 or i == 2) and (l == 0 or l == 2):
							dist_pixel[pos_y][pos_x] = sqrt(2)		#KALO DI POJOK SEARCH WINDOW
						else:
							dist_pixel[pos_y][pos_x] = 1			#KALO DI KIRI/KANAN/ATAS/BAWAH
					print dist_pixel[pos_y][pos_x]
			col += 1
		row += 1
	print(dist_pixel)
	return dist_pixel

if __name__ == '__main__':
	Lkimg = central_filter.parseInputPixel("L7SR.05-24-01.txt")
	Mkimg = central_filter.parseInputPixel("MOD09GHK.05-24-01.green.txt")
	M0img = central_filter.parseInputPixel("MOD09GHK.06-04-01.green.txt")
	
	central_pixel = central_filter.getCentralPixel(Lkimg)
	classified_pixel = central_filter.unsupervisedClassification(Lkimg, central_pixel)

	spec_diff = compute_diff(Lkimg, Mkimg)
	temporal_diff = compute_diff(Mkimg, M0img)
	dist_pixel = compute_distance(classified_pixel, central_pixel)