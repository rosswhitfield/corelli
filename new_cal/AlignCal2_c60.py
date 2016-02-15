#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/new_cal/c60_sn8.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-15,242-256")

componentList2=""
for i in range(47,62):
    componentList2+="bank"+str(i)+"/sixteenpack,"

componentList2=componentList2[:-1]
print componentList2

# rows - Y
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="B row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()


# CL1
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='alignedWorkspace',EulerConvention="YXZ",ComponentList=componentList2,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True,MinAlphaRotation=-20,MaxAlphaRotation=20)

ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_C60.xml',EulerConvention='YXZ',Components=componentList2)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_C60.nxs')
