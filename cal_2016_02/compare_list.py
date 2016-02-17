#!/usr/bin/env python2
import sys
import numpy as np

new=np.loadtxt(sys.argv[1],skiprows=1,usecols=(1,2,3,4,5,6))
try:
    compare_file=sys.argv[2]
    org=np.loadtxt(compare_file,skiprows=1,usecols=(1,2,3,4,5,6))
except:
    compare_file='/home/rwp/mantidgeometry/SNS/CORELLI/CORELLI_geom.txt'
    org=np.loadtxt(compare_file,skiprows=1,usecols=(4,5,6,7,8,9))

diff=new-org
np.set_printoptions(precision=2,suppress=True,edgeitems=10)

#print diff
i=1
for line in diff:
    print "bank"+str(i),line
    i+=1
