import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calib.txt')

data_org=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47301.nxs.h5',BankName='bank33,bank45,bank57')

data=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47301.nxs.h5',BankName='bank33,bank45,bank57')

ApplyCalibration(data,'CalibTable')
