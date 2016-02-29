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
