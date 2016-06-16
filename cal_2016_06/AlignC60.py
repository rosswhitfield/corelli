#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_06/cal_C60_20501-8_sum4_mask_lt_3_MaxChiSq3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")
#MaskBTP(Workspace='C60_mask',Bank="15,16,19,20,21,47,51,52,77,78,81,82,83")

componentList1=""
for i in range(1,92):
    componentList1+="bank"+str(i)+"/sixteenpack,"

componentList1=componentList1[:-1]
print componentList1

# rows - Y
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",ComponentList="A row,B row,C row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()


AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='alignedWorkspace',EulerConvention='YXZ',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_06/AlignC60.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_06/AlignC60.nxs')
