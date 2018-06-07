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

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/calB_c60.h5',InstrumentName='CORELLI',WorkspaceName='c60B')
difc_c60B=CalculateDIFC('corelli',CalibrationWorkspace='c60B_cal')
diff_c60B = difc_c60B/difc



corelli_y2=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli_y2','CalibTable')
y=0.02
MoveInstrumentComponent(Workspace='corelli_y2',ComponentName='A row',Y=y,RelativePosition=False)
MoveInstrumentComponent(Workspace='corelli_y2',ComponentName='B row',Y=y,RelativePosition=False)
MoveInstrumentComponent(Workspace='corelli_y2',ComponentName='C row',Y=y,RelativePosition=False)
difc_y2=CalculateDIFC('corelli_y2')



LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/cal_c60_y_0.02.h5',InstrumentName='CORELLI',WorkspaceName='c60_y2')
difc_c60_y2=CalculateDIFC('corelli',CalibrationWorkspace='c60_y2_cal')
diff_c60_y2 = difc_c60_y2/difc_y2

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/0/calB_c60_y_0.02.h5',InstrumentName='CORELLI',WorkspaceName='c60B_y2')
difc_c60B_y2=CalculateDIFC('corelli',CalibrationWorkspace='c60B_y2_cal')
diff_c60B_y2 = difc_c60B_y2/difc_y2


y=0.5
LoadEmptyInstrument(InstrumentName='CORELLI',OutputWorkspace='corelli_y_{}'.format(y))
ApplyCalibration('corelli_y_{}'.format(y),'CalibTable')
MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='A row',Y=y,RelativePosition=False)
MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='B row',Y=y,RelativePosition=False)
MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='C row',Y=y,RelativePosition=False)
CalculateDIFC('corelli_y_{}'.format(y), OutputWorkspace='difc_y_{}'.format(y))
Divide('difc_y_{}'.format(y),difc,OutputWorkspace='diff_y_{}'.format(y))


for y in np.arange(-0.05,0.06,0.01):
    CloneWorkspace('corelli',OutputWorkspace='corelli_y_{}'.format(y))
    MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='A row',Y=y,RelativePosition=False)
    MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='B row',Y=y,RelativePosition=False)
    MoveInstrumentComponent(Workspace='corelli_y_{}'.format(y),ComponentName='C row',Y=y,RelativePosition=False)
    CalculateDIFC('corelli_y_{}'.format(y), OutputWorkspace='difc_y_{}'.format(y))
    Divide('difc_y_{}'.format(y),difc,OutputWorkspace='diff_y_{}'.format(y))


angle=5
LoadEmptyInstrument(InstrumentName='CORELLI',OutputWorkspace='corelli_a_{}'.format(angle))
ApplyCalibration('corelli_a_{}'.format(angle),'CalibTable')
RotateInstrumentComponent(Workspace='corelli_a_{}'.format(angle),ComponentName='A row',Y=1,Angle=angle,RelativeRotation=False)
RotateInstrumentComponent(Workspace='corelli_a_{}'.format(angle),ComponentName='B row',Y=1,Angle=angle,RelativeRotation=False)
RotateInstrumentComponent(Workspace='corelli_a_{}'.format(angle),ComponentName='C row',Y=1,Angle=angle,RelativeRotation=False)
CalculateDIFC('corelli_a_{}'.format(angle), OutputWorkspace='difc_a_{}'.format(angle))
Divide('difc_a_{}'.format(angle),difc,OutputWorkspace='diff_a_{}'.format(angle))
