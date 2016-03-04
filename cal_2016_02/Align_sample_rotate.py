from mantid.simpleapi import *

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20025_sum4_mask_lt_3.cal', WorkspaceName='D0')
MaskBTP(Workspace='D0_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20026_sum4_mask_lt_3.cal', WorkspaceName='D45')
MaskBTP(Workspace='D45_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20027_sum4_mask_lt_3.cal', WorkspaceName='D90')
MaskBTP(Workspace='D90_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="D0_cal",MaskWorkspace="D0_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()
AlignComponents(CalibrationTable="D45_cal",MaskWorkspace="D45_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()
AlignComponents(CalibrationTable="D90_cal",MaskWorkspace="D90_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()

# D0  [-0.0047747,-0.0083195,0.00325148]
# D45 [-0.00584546,-0.00831521,0.00449592]
# D90 [-0.0061939,-0.00826052,0.0052628]
from matplotlib import pyplot as plt
x=[-0.0047747,-0.00584546,-0.0061939]
y=[0.00325148,0.00449592,0.0052628]
plt.scatter(x,y)
plt.show()


LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_19675_sum4_mask_lt_3.cal', WorkspaceName='D0')
MaskBTP(Workspace='D0_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_19676_sum4_mask_lt_3.cal', WorkspaceName='D45')
MaskBTP(Workspace='D45_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_19677_sum4_mask_lt_3.cal', WorkspaceName='D90')
MaskBTP(Workspace='D90_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_19678_sum4_mask_lt_3.cal', WorkspaceName='D135')
MaskBTP(Workspace='D135_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="D0_cal",MaskWorkspace="D0_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()
AlignComponents(CalibrationTable="D45_cal",MaskWorkspace="D45_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()
AlignComponents(CalibrationTable="D90_cal",MaskWorkspace="D90_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()
AlignComponents(CalibrationTable="D135_cal",MaskWorkspace="D135_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos()

# D0   [-0.0017193,-0.00648433,0.00593814]
# D45  [-0.00198862,-0.00633684,0.00685791]
# D90  [-0.000965499,-0.00640095,0.00726321]
# D135 [0.00155763,-0.00649624,0.00693169]
x=[-0.0017193,-0.00198862,-0.000965499,0.00155763]
y=[0.00593814,0.00685791,0.00726321,0.00693169]
plt.scatter(x,y,color='red')
plt.show()

# Si [0.00322408,-0.00533446,0.00491069]
# LaB6 [-0.000253892,-0.0071092,0.00605707]
# C60 [-0.00102155,-0.00652617,0.00708104]
# D [-0.00545487,-0.00859597,0.00441433]

x=[0.00322408,-0.000253892,-0.00102155,-0.00545487]
y=[0.00491069,0.00605707,0.00708104,0.00441433]
plt.scatter(x,y,color='green')
plt.show()


# New Diamond

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20482_sum4_mask_lt_3.cal', WorkspaceName='D0')
MaskBTP(Workspace='D0_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20483_sum4_mask_lt_3.cal', WorkspaceName='D45')
MaskBTP(Workspace='D45_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20484_sum4_mask_lt_3.cal', WorkspaceName='D90')
MaskBTP(Workspace='D90_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20485_sum4_mask_lt_3.cal', WorkspaceName='D125')
MaskBTP(Workspace='D125_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20486_sum4_mask_lt_3.cal', WorkspaceName='D180')
MaskBTP(Workspace='D180_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20487_sum4_mask_lt_3.cal', WorkspaceName='D225')
MaskBTP(Workspace='D225_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20488_sum4_mask_lt_3.cal', WorkspaceName='D270')
MaskBTP(Workspace='D270_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Diamond_20489_sum4_mask_lt_3.cal', WorkspaceName='D315')
MaskBTP(Workspace='D315_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="D0_cal",MaskWorkspace="D0_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.000321203,-0.00831816,-0.00202766]
AlignComponents(CalibrationTable="D45_cal",MaskWorkspace="D45_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00222277,-0.00819707,-0.000758006]
AlignComponents(CalibrationTable="D90_cal",MaskWorkspace="D90_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00430158,-0.00817648,0.00178252]
AlignComponents(CalibrationTable="D125_cal",MaskWorkspace="D125_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00535637,-0.00809624,0.00390734]
AlignComponents(CalibrationTable="D180_cal",MaskWorkspace="D180_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00499453,-0.00808678,0.00458609]
AlignComponents(CalibrationTable="D225_cal",MaskWorkspace="D225_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00327941,-0.00813107,0.003294]
AlignComponents(CalibrationTable="D270_cal",MaskWorkspace="D270_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.00111812,-0.0082369,0.00078521]
AlignComponents(CalibrationTable="D315_cal",MaskWorkspace="D315_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.000161658,-0.00828212,-0.00141538]

x=[-0.000321203,-0.00222277,-0.00430158,-0.00535637,-0.00499453,-0.00327941,-0.00111812,0.000161658]
y=[-0.00202766,-0.000758006,0.00178252,0.00390734,0.00458609,0.003294,0.00078521,-0.00141538]
plt.scatter(x,y)
plt.show()

x=[-0.00268209,-0.00415737,-0.00562921,-0.00758637]
y=[0.00143682,-0.00204993,-0.00553504,-0.0101793]
plt.scatter(x,y,color='red')
plt.show()

# Si

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20492_sum4_mask_lt_3.cal', WorkspaceName='Si0')
MaskBTP(Workspace='Si0_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20493_sum4_mask_lt_3.cal', WorkspaceName='Si45')
MaskBTP(Workspace='Si45_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20494_sum4_mask_lt_3.cal', WorkspaceName='Si90')
MaskBTP(Workspace='Si90_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20495_sum4_mask_lt_3.cal', WorkspaceName='Si125')
MaskBTP(Workspace='Si125_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20496_sum4_mask_lt_3.cal', WorkspaceName='Si180')
MaskBTP(Workspace='Si180_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20497_sum4_mask_lt_3.cal', WorkspaceName='Si225')
MaskBTP(Workspace='Si225_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20498_sum4_mask_lt_3.cal', WorkspaceName='Si270')
MaskBTP(Workspace='Si270_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_20499_sum4_mask_lt_3.cal', WorkspaceName='Si315')
MaskBTP(Workspace='Si315_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="Si0_cal",MaskWorkspace="Si0_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.000709988,-0.00682142,0.00736992]
AlignComponents(CalibrationTable="Si45_cal",MaskWorkspace="Si45_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.000742807,-0.00666427,0.00681258]
AlignComponents(CalibrationTable="Si90_cal",MaskWorkspace="Si90_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00288301,-0.0068174,0.00548946]
AlignComponents(CalibrationTable="Si125_cal",MaskWorkspace="Si125_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00423735,-0.006871,0.00404843]
AlignComponents(CalibrationTable="Si180_cal",MaskWorkspace="Si180_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00481421,-0.00680394,0.00308387]
AlignComponents(CalibrationTable="Si225_cal",MaskWorkspace="Si225_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00412373,-0.00673156,0.00283841]
AlignComponents(CalibrationTable="Si270_cal",MaskWorkspace="Si270_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.000849782,-0.00684171,0.00454779]
AlignComponents(CalibrationTable="Si315_cal",MaskWorkspace="Si315_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.0020792,-0.00699353,0.00699872]

x=[-0.000709988,0.000742807,0.00288301,0.00423735,0.00481421,0.00412373,0.000849782,-0.0020792]
y=[0.00736992,0.00681258,0.00548946,0.00404843,0.00308387,0.00283841,0.00454779,0.00699872]
plt.scatter(x,y,color='red')
plt.show()

# C60

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501_sum4_mask_lt_3.cal', WorkspaceName='C60_0')
MaskBTP(Workspace='C60_0_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20502_sum4_mask_lt_3.cal', WorkspaceName='C60_45')
MaskBTP(Workspace='C60_45_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20503_sum4_mask_lt_3.cal', WorkspaceName='C60_90')
MaskBTP(Workspace='C60_90_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20504_sum4_mask_lt_3.cal', WorkspaceName='C60_125')
MaskBTP(Workspace='C60_125_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20505_sum4_mask_lt_3.cal', WorkspaceName='C60_180')
MaskBTP(Workspace='C60_180_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20506_sum4_mask_lt_3.cal', WorkspaceName='C60_225')
MaskBTP(Workspace='C60_225_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20507_sum4_mask_lt_3.cal', WorkspaceName='C60_270')
MaskBTP(Workspace='C60_270_mask',Pixel="1-16,241-256")
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20508_sum4_mask_lt_3.cal', WorkspaceName='C60_315')
MaskBTP(Workspace='C60_315_mask',Pixel="1-16,241-256")

AlignComponents(CalibrationTable="C60_0_cal",MaskWorkspace="C60_0_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.000993467,-0.00664731,0.00599745]
AlignComponents(CalibrationTable="C60_45_cal",MaskWorkspace="C60_45_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [-0.000863118,-0.00655385,0.00684611]
AlignComponents(CalibrationTable="C60_90_cal",MaskWorkspace="C60_90_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.000750809,-0.00660043,0.00693584]
AlignComponents(CalibrationTable="C60_125_cal",MaskWorkspace="C60_125_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00292343,-0.00646138,0.00634512]
AlignComponents(CalibrationTable="C60_180_cal",MaskWorkspace="C60_180_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00445923,-0.00666753,0.00570071]
AlignComponents(CalibrationTable="C60_225_cal",MaskWorkspace="C60_225_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00442895,-0.00659322,0.00523587]
AlignComponents(CalibrationTable="C60_270_cal",MaskWorkspace="C60_270_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00274747,-0.00656127,0.00497561]
AlignComponents(CalibrationTable="C60_315_cal",MaskWorkspace="C60_315_mask",InstrumentFilename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['alignedWorkspace'].getInstrument().getSample().getPos() # [0.00170466,-0.00666564,0.00499505]

x=[-0.000993467,-0.000863118,0.000750809,0.00292343,0.00445923,0.00442895,0.00274747,0.00170466]
y=[0.00599745,0.00684611,0.00693584,0.00634512,0.00570071,0.00523587,0.00497561,0.00499505]
plt.scatter(x,y,color='green')
plt.show()

x=[0.00184122,0.00184901,-0.00268209]
y=[0.00576574,0.0060678,0.00143682]
plt.scatter(x,y,color='black')
plt.show()

# Move souce first. Z=-20.04
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si0_cal",MaskWorkspace="Si0_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.0026684,-0.00694497,-0.000500656]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si45_cal",MaskWorkspace="Si45_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00118079,-0.00677887,-0.0010309]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si90_cal",MaskWorkspace="Si90_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.000986816,-0.00692187,-0.00232608]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si125_cal",MaskWorkspace="Si125_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00233288,-0.00698112,-0.00377158]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si180_cal",MaskWorkspace="Si180_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00293039,-0.0069161,-0.00471556]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si225_cal",MaskWorkspace="Si225_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [0.00225814,-0.00682836,-0.00494606]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si270_cal",MaskWorkspace="Si270_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00106886,-0.0069614,-0.00328831]
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='ws')
MoveInstrumentComponent(Workspace='ws',ComponentName='moderator',Z=-20.04,RelativePosition=False)
AlignComponents(CalibrationTable="Si315_cal",MaskWorkspace="Si315_mask",Workspace='ws',FitSamplePosition=True,Xposition=True,Yposition=True,Zposition=True)
print mtd['ws'].getInstrument().getSample().getPos() # [-0.00406143,-0.00714001,-0.000893758]

x=[-0.0026684,-0.00118079,0.000986816,0.00233288,0.00293039,0.00225814,-0.00106886,-0.00406143]
y=[-0.000500656,-0.0010309,-0.00232608,-0.00377158,-0.00471556,-0.00494606,-0.00328831,-0.000893758]
plt.scatter(x,y)
plt.show()
