#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/new_cal/c60_sn8.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Bank="1-46,62-91")
MaskBTP(Workspace='C60_mask',Pixel="1-15,242-256")

componentList2=""
for i in range(47,62):
    componentList2+="bank"+str(i)+"/sixteenpack,"

componentList2=componentList2[:-1]
print componentList2


# CL1
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",EulerConvention="YXZ",ComponentList=componentList2,Xposition=True,Yposition=True,Zposition=True)

ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_C60xyz.xml',EulerConvention='YXZ',Components=componentList2)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_C60xyz.nxs')
