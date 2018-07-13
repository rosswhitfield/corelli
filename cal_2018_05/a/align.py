import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
difc_old=CalculateDIFC('corelli')

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/a/cal.h5',InstrumentName='CORELLI',WorkspaceName='cal')

MaskBTP('mask',Bank='26',Tube='1-8')
MaskBTP('mask',Pixel='1-16,241-256')

# Kick them so they start moving
RotateInstrumentComponent('corelli', ComponentName='A row',Y=1,angle=0.01)
RotateInstrumentComponent('corelli', ComponentName='B row',Y=1,angle=0.01)
RotateInstrumentComponent('corelli', ComponentName='C row',Y=1,angle=0.01)

AlignComponents(Workspace='corelli',CalibrationTable="cal_cal",MaskWorkspace="cal_mask",ComponentList="A row,B row,C row",Xposition=True,Yposition=True,Zposition=True,AlphaRotation=True)
print(mtd['corelli'].getInstrument().getComponentByName('A row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('A row').getRotation().getEulerAngles())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getRotation().getEulerAngles())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getRotation().getEulerAngles())

SaveNexus('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned.nxs')

difc_new=CalculateDIFC('corelli')
difc_diff = difc_new/difc_old
