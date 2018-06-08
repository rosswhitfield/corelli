import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('corelli','/SNS/users/rwp/corelli/cal_2018_05/0a/Aligned_row_si_c60.nxs.detcal')

difc=CalculateDIFC('corelli')

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/1/cal_si.h5',InstrumentName='CORELLI',WorkspaceName='si')
difc_si=CalculateDIFC('corelli',CalibrationWorkspace='si_cal')
diff_si = difc_si/difc

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/1/calB_si.h5',InstrumentName='CORELLI',WorkspaceName='siB')
difc_siB=CalculateDIFC('corelli',CalibrationWorkspace='siB_cal')
diff_siB = difc_siB/difc

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/1/cal_c60.h5',InstrumentName='CORELLI',WorkspaceName='c60')
difc_c60=CalculateDIFC('corelli',CalibrationWorkspace='c60_cal')
diff_c60 = difc_c60/difc

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/1/calB_c60.h5',InstrumentName='CORELLI',WorkspaceName='c60B')
difc_c60B=CalculateDIFC('corelli',CalibrationWorkspace='c60B_cal')
diff_c60B = difc_c60B/difc

LoadDiffCal(Filename='/SNS/users/rwp/corelli/cal_2018_05/1/cal_si_c60.h5',InstrumentName='CORELLI',WorkspaceName='si_c60')
difc_si_c60=CalculateDIFC('corelli',CalibrationWorkspace='si_c60_cal')
diff_si_c60 = difc_si_c60/difc
