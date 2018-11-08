import sys
from paraview.simple import *
filename = sys.argv[1]
size = int(sys.argv[2])

vts = XMLStructuredGridReader(FileName=[filename])

image = ResampleToImage(vts)
image.SamplingDimensions = [size, size, size]

SaveData(filename.replace('vts','vti'), proxy=image)
