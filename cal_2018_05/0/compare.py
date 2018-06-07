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


