#!/usr/bin/env python2
from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_06/cal_Diamond_20482-9_sum4_mask_lt_3.cal', WorkspaceName='Diamond')
MaskBTP(Workspace='Diamond_mask',Pixel="1-16,241-256")

componentList1=""
for i in range(1,92):
    componentList1+="bank"+str(i)+"/sixteenpack,"

componentList1=componentList1[:-1]
print componentList1

# rows - Y
AlignComponents(CalibrationTable="Diamond_cal",MaskWorkspace="Diamond_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_91.07cm.xml",ComponentList="A row,B row,C row",Yposition=True)
print mtd['alignedWorkspace'].getInstrument().getComponentByName('A row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('B row').getPos()
print mtd['alignedWorkspace'].getInstrument().getComponentByName('C row').getPos()


AlignComponents(CalibrationTable="Diamond_cal",MaskWorkspace="Diamond_mask",Workspace='alignedWorkspace',EulerConvention='YXZ',ComponentList=componentList1,Xposition=True,Zposition=True,AlphaRotation=True,BetaRotation=True,GammaRotation=True)
ExportGeometry(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_06/AlignDiamond.xml',EulerConvention='YXZ',Components=componentList1)
SaveNexus(InputWorkspace='alignedWorkspace',Filename='/SNS/users/rwp/corelli/cal_2016_06/AlignDiamond.nxs')
