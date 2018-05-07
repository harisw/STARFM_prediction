import numpy as np
import central_filter

def compute_diff(first_img, second_img):
	diff_pixel = np.empty([1199, 1199], dtype=int)
	row = 0
	while(row < 1199):
		col = 0
		while(col < 1199):
			diff_pixel[row][col] = abs( first_img[row][col] - second_img[row][col])
			col += 1
		row += 1
	return np.array(diff_pixel)

if __name__ == '__main__':
	Lkimg = central_filter.parseInputPixel("L7SR.05-24-01.txt")
	Mkimg = central_filter.parseInputPixel("MOD09GHK.05-24-01.green.txt")
	M0img = central_filter.parseInputPixel("MOD09GHK.06-04-01.green.txt")
	
	central_pixel = central_pixel.getCentralPixel(Lkimg)
	classified_pixel = central_pixel.unsupervisedClassification(Lkimg, central_pixel)
	
	spec_diff = compute_diff(Lkimg, Mkimg)
	temporal_diff = compute_diff(Mkimg, M0img)