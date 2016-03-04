from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20492-9_sum4_mask_lt_3.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20482-9_sum4_mask_lt_3.cal', WorkspaceName='D')
MaskBTP(Workspace='D_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00184122,-0.00611992,0.00576574]
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00184901,-0.00673252,0.0060678]
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00268209,-0.00868087,0.00143682]

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # -20.0222
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # -20.0376
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # -20.0145


# Correct source position first Z=-20.05
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.000314165,-0.00616995,-0.00393096]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00186116,-0.00670434,8.53202e-05]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00758637,-0.00900499,-0.0101793]

# Correct source position first Z=-20.04
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.000116243,-0.00615996,-0.00199209]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00185874,-0.00670996,0.00128166]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00660855,-0.00894025,-0.00785756]

# Correct source position first Z=-20.03
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.000546987,-0.00614996,-5.29738e-05]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00185632,-0.00671559,0.00247806]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00562921,-0.00887545,-0.00553504]

# Correct source position first Z=-20.015
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00119372,-0.00613495,0.00285612]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00185267,-0.00672404,0.00427286]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="D_cal",MaskWorkspace="D_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00415737,-0.00877821,-0.00204993]
