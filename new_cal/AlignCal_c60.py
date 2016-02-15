#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/new_cal/c60_sn.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Bank="1-55,61-91")
MaskBTP(Workspace='C60_mask',Pixel="1-15,242-256")

# Source
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()

# Sample
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()

# B row - Y
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="B row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()

AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="B row",Yposition=True,Xposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()


componentList2=""
for i in range(56,61):
    componentList2+="bank"+str(i)+"/sixteenpack,"

componentList2=componentList2[:-1]
print componentList2

# CL1
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='alignedWorkspace')
MoveInstrumentComponent(Workspace='alignedWorkspace',ComponentName='B row',Y=0.007657542)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='alignedWorkspace',ComponentList=componentList2,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True,MinAlphaRotation=-20,MaxAlphaRotation=20)
for i in componentList2.split(','):
    print i,mtd['alignedWorkspace'].getInstrument().getComponentByName(i).getPos(),mtd['alignedWorkspace'].getInstrument().getComponentByName(i).getRotation().getEulerAngles("YXZ")

ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/c60_Brow+banks_xzabg.xml',EulerConvention='YXZ',Components=componentList2)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/c60_source_Brow+banks_xzabg.nxs')


# Refine source just using bank 58/59
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/new_cal/c60_sn.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Bank="1-57,60-91")
MaskBTP(Workspace='C60_mask',Pixel="1-15,242-256")
# Source
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()

# source at [0,0,-20.5204]

# banks 57-60
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/new_cal/c60_sn.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Bank="1-56,61-91")
MaskBTP(Workspace='C60_mask',Pixel="1-15,242-256")
# Source
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()

# source at [0,0,-20.2547]




# change reference, move bank?? not bank??/sixteenpack
componentList3=""
for i in range(56,61):
    componentList3+="bank"+str(i)+","

componentList3=componentList3[:-1]
print componentList3

LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='alignedWorkspace')
MoveInstrumentComponent(Workspace='alignedWorkspace',ComponentName='B row',Y=0.007657542)

# kick the banks
for i in componentList3.split(','):
    RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName=i,X=0,Y=1,Z=0,Angle=0.01)


AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='alignedWorkspace',ComponentList=componentList3,AlphaRotation=True)

for i in componentList3.split(','):
    print i,mtd['alignedWorkspace'].getInstrument().getComponentByName(i).getPos(),mtd['alignedWorkspace'].getInstrument().getComponentByName(i).getRotation().getEulerAngles("YXZ")

# kick the banks
for i in componentList3.split(','):
    RotateInstrumentComponent(Workspace='alignedWorkspace',ComponentName=i,X=1,Y=1,Z=1,Angle=0.01)


AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='alignedWorkspace',ComponentList=componentList3,AlphaRotation=True,BetaRotation=True,GammaRotation=True)

for i in componentList3.split(','):
    print i,mtd['alignedWorkspace'].getInstrument().getComponentByName(i).getPos(),mtd['alignedWorkspace'].getInstrument().getComponentByName(i).getRotation().getEulerAngles("YXZ")

