import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/calB_si.h5',InstrumentName='CORELLI',WorkspaceName='si')
LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/cal_si_c60.h5',InstrumentName='CORELLI',WorkspaceName='cal')
BinaryOperateMasks('cal_mask','si_mask', OutputWorkspace='mask')

MaskBTP('cal_mask',Bank='26',Tube='1-8')
MaskBTP('cal_mask',Pixel='1-16,241-256')

# rows - Y
AlignComponents(Workspace='corelli',CalibrationTable="cal_cal",MaskWorkspace="cal_mask",ComponentList="A row,B row,C row",Xposition=True,Yposition=True,Zposition=True,AlphaRotation=True)
print(mtd['corelli'].getInstrument().getComponentByName('A row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getPos())
print(mtd['corelli'].getInstrument().getComponentByName('A row').getRotation().getEulerAngles())
print(mtd['corelli'].getInstrument().getComponentByName('B row').getRotation().getEulerAngles())
print(mtd['corelli'].getInstrument().getComponentByName('C row').getRotation().getEulerAngles())
