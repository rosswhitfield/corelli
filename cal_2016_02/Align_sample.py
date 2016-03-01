from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_19284_19285_sum4_mask_lt_3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_LaB6_19286_19287_sum4_mask_lt_3.cal', WorkspaceName='LaB6')
MaskBTP(Workspace='LaB6_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_19674-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='LaB6_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20025-7_sum4_mask_lt_3.cal', WorkspaceName='D')
MaskBTP(Workspace='LaB6_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00322408,-0.00533446,0.00491069]
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.000253892,-0.0071092,0.00605707]
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00102155,-0.00652617,0.00708104]
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00545487,-0.00859597,0.00441433]

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [-0.020983,0.0420465,-20.0249] / -20.0135
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [0.00766962,0.0569411,-20.0237] / -20.0297
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [0.00767057,0.0537578,-20.0587] / -20.0659
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [0.068594,0.0570005,-19.9943] / -20.0366
