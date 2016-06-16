#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_06/cal_Si_20492-9_sum4_mask_lt_3_MaxChiSq3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
MaskBTP(Workspace='Si_mask',Bank="55-61")

componentList1=""
for i in range(1,92):
    componentList1+="bank"+str(i)+"/sixteenpack,"

componentList1=componentList1[:-1]
print componentList1

# rows - Y
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",ComponentList="A row,B row,C row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()


AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='alignedWorkspace',EulerConvention='YXZ',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_06/AlignSi.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_06/AlignSi.nxs')
