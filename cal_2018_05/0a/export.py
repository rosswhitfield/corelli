import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('corelli','CalibTable')
LoadIsawDetCal('rawC60','/SNS/users/rwp/corelli/cal_2018_05/0a/Aligned_row_si_c60.nxs.detcal')
