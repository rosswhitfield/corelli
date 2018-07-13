import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/57_80/out')

data = Load('CORELLI_59293-59296', BankName='bank57,bank80')
org = CloneWorkspace(data)

ApplyCalibration(data,'CalibTable')

tube.readCalibrationFile('CalibTable2','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')
ApplyCalibration(data,'CalibTable2')
