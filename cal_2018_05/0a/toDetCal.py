#!/usr/bin/env python2
import sys
from mantid.simpleapi import *

workspace_filename = sys.argv[1]

cal=LoadNexus(Filename=workspace_filename)
i=cal.getInstrument()

print("Location Xsci Ysci Zsci Xrot_sci Yrot_sci Zrot_sci")

for bank in range(1,92):
    b=i.getComponentByName("bank"+str(bank)+"/sixteenpack")
    x=b.getPos().getX()*100 # cm
    y=b.getPos().getY()*100 # cm
    z=b.getPos().getZ()*100 # cm
    [beta,alpha,gamma]=b.getRotation().getEulerAngles("YXZ")
    print('5 {:4}   16   256   20.00  78.00  0.20  10.00 '.format(bank,x,y,z,alpha,beta,gamma))
