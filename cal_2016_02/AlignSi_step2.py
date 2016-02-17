#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/corelli/cal_2016_02/CORELLI_Definition_AlignSi.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_19284_19285_sum4_step2.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")

componentList1=""
for i in range(1,91):
    componentList1+="bank"+str(i)+"/sixteenpack,"

componentList1=componentList1[:-1]
print componentList1

# rows - Y
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/corelli/cal_2016_02/CORELLI_Definition_AlignSi.xml",ComponentList="A row,B row,C row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()


AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',EulerConvention='YXZ',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True,MinAlphaRotation=-20,MaxAlphaRotation=20)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_02/AlignSi_step2.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_02/AlignSi_step2.nxs')
