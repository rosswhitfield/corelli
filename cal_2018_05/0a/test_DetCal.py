import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

org=LoadNexus(Filename='Aligned_row_si_c60.nxs')

new=LoadEmptyInstrument(InstrumentName='CORELLI')
ApplyCalibration('new','CalibTable')

LoadIsawDetCal('new','/SNS/users/rwp/corelli/cal_2018_05/0a/Aligned_row_si_c60.nxs.detcal')
difc_check=CalculateDIFC('new')
diff_check = difc_check/difc
