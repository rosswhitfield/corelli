#!/usr/bin/env python2
import sys
import numpy as np

new=np.loadtxt(sys.argv[1],skiprows=1,usecols=(1,2,3,4,5,6))
org=np.loadtxt('/home/rwp/mantidgeometry/SNS/CORELLI/CORELLI_geom.txt',skiprows=1,usecols=(4,5,6,7,8,9))

diff=new-org
np.set_printoptions(precision=2,suppress=True)
print diff
