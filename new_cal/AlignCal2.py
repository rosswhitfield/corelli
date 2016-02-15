#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/new_cal/cal_run14324_sn8.dat', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-15,242-256")

componentList1=""
for i in range(1,91):
    componentList1+="bank"+str(i)+"/sixteenpack,"

componentList1=componentList1[:-1]
print componentList1

# rows - Y
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",ComponentList="A row,B row,C row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()


AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',EulerConvention='YXZ',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True,MinAlphaRotation=-20,MaxAlphaRotation=20)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_si.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/new_cal/AlignCal2_si.nxs')
