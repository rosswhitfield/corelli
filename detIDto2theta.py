from mantid.simpleapi import *
from mantid.kernel import V3D
import math
c=LoadEmptyInstrument(OutputWorkspace='cor',Filename='/SNS/users/rwp/CORELLI_Definition.xml')

for i in range(91*16*256):
    print i, c.getDetector(i+3).getTwoTheta(V3D(0,0,0),V3D(0,0,1))*180/math.pi
