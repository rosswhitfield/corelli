#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/new_cal/c60_sn8.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Bank="1-56,61-91")
MaskBTP(Workspace='C60_mask',Pixel="1-15,242-256")

componentList2=""
for i in range(57,61):
    for j in range(1,17):
        componentList2+="bank"+str(i)+"/sixteenpack/tube"+str(j)+','

componentList2=componentList2[:-1]
print componentList2


# CL1
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",EulerConvention="YXZ",ComponentList=componentList2,Xposition=True,Zposition=True)

ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_C60_tubes.xml',EulerConvention='YXZ',Components=componentList2)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_C60_tubes.nxs')
