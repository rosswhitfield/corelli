from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_19284_19285_sum4_mask_lt_3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_LaB6_19286_19287_sum4_mask_lt_3.cal', WorkspaceName='LaB6')
MaskBTP(Workspace='LaB6_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_19674-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20025-7_sum4_mask_lt_3.cal', WorkspaceName='D')
MaskBTP(Workspace='D_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20482-9_sum4_mask_lt_3.cal', WorkspaceName='D2')
MaskBTP(Workspace='D2_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00322408,-0.00533446,0.00491069]
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.000253892,-0.0071092,0.00605707]
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00102155,-0.00652617,0.00708104]
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00545487,-0.00859597,0.00441433]
AlignComponents(CalibrationTable="D2_cal",MaskWorkspace="D2_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00268209,-0.00868087,0.00143682]

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [-0.020983,0.0420465,-20.0249] / -20.0135
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [0.00766962,0.0569411,-20.0237] / -20.0297
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [0.00767057,0.0537578,-20.0587] / -20.0659
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # [0.068594,0.0570005,-19.9943] / -20.0366
AlignComponents(CalibrationTable="D2_cal",MaskWorkspace="D2_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # -20.0145


# Correct source position first Z=-20.05
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00112348,-0.00538002,-0.00471899]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.0013651,-0.00702317,-0.00284807]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00100911,-0.00649803,0.00110101]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.0104108,-0.0088928,-0.00723241]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="D2_cal",MaskWorkspace="D2_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00758637,-0.00900499,-0.0101793]

# Correct source position first Z=-20.03
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00196276,-0.00536183,-0.000867792]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.000920997,-0.00705747,0.000713426]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00101407,-0.00650926,0.00349279]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00843304,-0.00877422,-0.00257591]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="D2_cal",MaskWorkspace="D2_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00562921,-0.00887545,-0.00553504]

# Correct source position first Z=-20.015
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00259306,-0.00534815,0.0020212]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="LaB6_cal",MaskWorkspace="LaB6_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.000587586,-0.00708329,0.00338504]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00102031,-0.00650518,0.00527882]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00694254,-0.00867724,0.000918924]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="D2_cal",MaskWorkspace="D2_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00415737,-0.00877821,-0.00204993]

