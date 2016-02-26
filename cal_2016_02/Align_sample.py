from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_19284_19285_sum4_mask_lt_3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_LaB6_19286_19287_sum4_mask_lt_3.cal', WorkspaceName='LaB6')
MaskBTP(Workspace='LaB6_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_19674-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='LaB6_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos()
