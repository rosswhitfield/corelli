import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calib2.txt')

data_org=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47301.nxs.h5',BankName='bank33,bank45,bank57')
data=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47301.nxs.h5',BankName='bank33,bank45,bank57')

ApplyCalibration(data,'CalibTable')




tube.readCalibrationFile('CalibTable2','/SNS/users/rwp/corelli/tube_calibration/calib2.txt')

data_org2=Load('CORELLI_47301+47034',BankName='bank33,bank45,bank57')
data2=Load('CORELLI_47301+47034',BankName='bank33,bank45,bank57')

ApplyCalibration(data,'CalibTable2')
