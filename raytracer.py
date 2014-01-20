import sys
from struct import *

def draw(outputFile, scene):
	"""
	Opens output file, writes header, then writes to buffer pixel by pixel,
	performing raytracing logic on each pixel
	"""
	#Opens output file
	output = open(outputFile, 'wb')
	
	#Creates header to write to buffer (initializer)
	header = pack('BBBBBBBBHHHHBB',
				  0, 0, 2, 0, 0, 0, 0, 0, 0, 0,
				  scene.getWidth(), scene.getHeight(),24, 0)
	output.write(header)
	
	#Iterates through every pixel in the scene, performs raytracing logic (getPixel),
	#adds new pixel to dictionary
	n = 0
	pixelDict = dict()
	for y in range(scene.getHeight()):
		for x in range(scene.getWidth()):
			pixelDict[n] = getPixel(x, y, scene)
			n += 1
	
	#Packs each individual pixel, writes it to output .tga file		
	pixelBuffer = ''
	for i, pixel in pixelDict.items():
		pixelBuffer += pack('BBB', pixel.b, pixel.g, pixel.r)
	output.write(pixelBuffer)

if __name__ == "__main__":
	"""
	Reads in file from std in, parses it for scene, then draws the new image.

	Instructions: python raytracer.py input/sample_input.txt output/outputfile.tga
	"""
	args = sys.argv[1:]
	s = Scene(args[0])
	draw(args[1], s)
