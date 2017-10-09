import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/out')

data=LoadNexus('/SNS/users/rwp/corelli/tube_calibration/all_banks.nxs')
org=CloneWorkspace(data)
ApplyCalibration(data,'CalibTable')
