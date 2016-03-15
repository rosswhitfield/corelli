from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20492-9_sum4_mask_lt_3_MaxChiSq_2.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3_MaxChiSq_5.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00212501,-0.00618488,0.00612001]
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.000551182,-0.0063023,0.0126171]

AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # -20.0246
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSourcePosition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSource().getPos() # -20.1


# Correct source position first Z=-20.05
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.000342883,-0.00622909,-0.00310111]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.05,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.000551142,-0.00629535,0.00672197]

# Correct source position first Z=-20.04
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.000698639,-0.00622027,-0.00125746]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00055115,-0.00629673,0.00790094]

# Correct source position first Z=-20.03
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00105471,-0.00621144,0.000586466]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.03,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00055116,-0.00629813,0.00907986]

# Correct source position first Z=-20.015
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="Si_cal",MaskWorkspace="Si_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00158948,-0.00619817,0.00335291]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.015,RelativePosition=False)
AlignComponents(CalibrationTable="C60_cal",MaskWorkspace="C60_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00055117,-0.00630022,0.0108484]
