from mantid.simpleapi import *
import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned3.nxs.detcal')

SaveNexus('corelli','/SNS/users/rwp/corelli/cal_2018_05/a/TubeCalib+DetCal.nxs')
