import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calib.txt')

data_org=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47301.nxs.h5',BankName='bank33,bank45,bank57')
data=LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47301.nxs.h5',BankName='bank33,bank45,bank57')

ApplyCalibration(data,'CalibTable')


tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calib.txt')

data_org=Load('CORELLI_47301-47304',BankName='bank33,bank45,bank57')
data=Load('CORELLI_47301-47304',BankName='bank33,bank45,bank57')

ApplyCalibration(data,'CalibTable')


tube.readCalibrationFile('CalibTable2','/SNS/users/rwp/corelli/tube_calibration/calib2.txt')

data2=Load('CORELLI_47301-47304',BankName='bank33,bank45,bank57')

ApplyCalibration(data2,'CalibTable2')


tube.readCalibrationFile('CalibTable3','/SNS/users/rwp/corelli/tube_calibration/calib3.txt')

data3=Load('CORELLI_47301-47304',BankName='bank33,bank45,bank57')

ApplyCalibration(data3,'CalibTable3')



# NEW
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calib.txt')

data_org=Load('CORELLI_47307',BankName='bank27,bank28,bank59,bank60,bank61')
data=CloneWorkspace(data_org)

ApplyCalibration(data,'CalibTable')



tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration/calib_all.txt')

tube.readCalibrationFile('CalibTable2000','/SNS/users/rwp/corelli/tube_calibration/calib_all_2000.txt')
