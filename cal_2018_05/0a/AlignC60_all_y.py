import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/cal_c60.h5',InstrumentName='CORELLI',WorkspaceName='c60')

# rows - Y
AlignComponents(Workspace='corelli',CalibrationTable="c60_cal",MaskWorkspace="c60_mask",ComponentList="A row,B row,C row",Yposition=True)
print(mtd['corelli'].getInstrument().getComponentByName('A row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getPos())

# Kick them so they start moving
RotateInstrumentComponent('corelli', ComponentName='A row',Y=1,angle=0.01)
RotateInstrumentComponent('corelli', ComponentName='B row',Y=1,angle=0.01)
RotateInstrumentComponent('corelli', ComponentName='C row',Y=1,angle=0.01)

AlignComponents(Workspace='corelli',CalibrationTable="c60_cal",MaskWorkspace="c60_mask",ComponentList="A row,B row,C row",Yposition=True,AlphaRotation=True)
print(mtd['corelli'].getInstrument().getComponentByName('A row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('A row').getRotation().getEulerAngles())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getRotation().getEulerAngles())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getRotation().getEulerAngles())
