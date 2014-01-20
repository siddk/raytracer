import sys


if __name__ == "__main__":
	"""
	Reads in file from std in, parses it for scene, then draws the new image.

	Instructions: python raytracer.py input/sample_input.txt output/outputfile.tga
	"""
	args = sys.argv[1:]
	s = Scene(args[0])
	draw(args[1], s)
