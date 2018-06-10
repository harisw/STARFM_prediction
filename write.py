from math import sqrt
from tqdm import tqdm
import numpy as np

pixel_dimension = 1125

def writePixel(pixel_result, target_file, pixel_type='regular'):
	print "Writing result to file\n"
	offset = len(pixel_result[0])
	bar = tqdm(total=offset)
	with open(target_file, 'w') as output_file:
		row = 0
		output_file.write(";\n")
		output_file.write("; ENVI ASCII Output\n")
		output_file.write("; File Dimensions: "+str(pixel_dimension)+" samples x "+str(pixel_dimension)+" lines x 1 band\n")
		output_file.write("; Line Format    : ("+str(pixel_dimension)+"i7)\n")
		output_file.write(";\n")
		while(row<offset):
			col = 0
			one_row = "    "
			while(col < offset):
				if pixel_type == 'final':
					temp = int(pixel_result[row][col])
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