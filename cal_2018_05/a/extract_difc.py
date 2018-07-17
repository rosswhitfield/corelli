import numpy as np
from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
difc=CalculateDIFC('corelli')
np.savetxt('difc_org.txt', difc.extractY().flatten())

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned.nxs.detcal')
difc=CalculateDIFC('corelli')
np.savetxt('difc_aligned.txt', difc.extractY().flatten())

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned2.nxs.detcal')
difc=CalculateDIFC('corelli')
np.savetxt('difc_aligned2.txt', difc.extractY().flatten())

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned3.nxs.detcal')
difc=CalculateDIFC('corelli')
np.savetxt('difc_aligned3.txt', difc.extractY().flatten())
