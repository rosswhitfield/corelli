import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/calB_si.h5',InstrumentName='CORELLI',WorkspaceName='si')

difc=CalculateDIFC('corelli')
difc_si=CalculateDIFC('corelli',CalibrationWorkspace='si_cal')

diff_si = difc_si/difc


LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/cal_c60.h5',InstrumentName='CORELLI',WorkspaceName='c60')

difc_c60=CalculateDIFC('corelli',CalibrationWorkspace='c60_cal')

diff_c60 = difc_c60/difc


y=0.5
LoadEmptyInstrument(InstrumentName='CORELLI',OutputWorkspace='corelli_y_{}'.format(y))
ApplyCalibration('corelli_y_{}'.format(y),'CalibTable')
MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='A row',Y=y,RelativePosition=False)
MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='B row',Y=y,RelativePosition=False)
MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='C row',Y=y,RelativePosition=False)
CalculateDIFC('corelli_y_{}'.format(y), OutputWorkspace='difc_y_{}'.format(y))
Divide('difc_y_{}'.format(y),difc,OutputWorkspace='diff_y_{}'.format(y))


for y in np.arange(-0.1,0.15,0.05):
    CloneWorkspace('corelli',OutputWorkspace='corelli_y_{}'.format(y))
    MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='A row',Y=y,RelativePosition=False)
    MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='B row',Y=y,RelativePosition=False)
    MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='C row',Y=y,RelativePosition=False)
    CalculateDIFC('corelli_y_{}'.format(y), OutputWorkspace='difc_y_{}'.format(y))
    Divide('difc_y_{}'.format(y),difc,OutputWorkspace='diff_y_{}'.format(y))

