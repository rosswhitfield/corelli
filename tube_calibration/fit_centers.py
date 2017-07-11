import numpy as np

centers=np.loadtxt('centers')

for row in centers:
    pixel = row[3:]
    print(pixel)
