import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2.txt')

ipts=18479

runs = [59288,59291]
filenames = '+'.join('/SNS/CORELLI/IPTS-{}/nexus/CORELLI_{}.nxs.h5'.format(ipts, r) for r in range(int(runs[0]), int(runs[1])+1))

data1=Load(filenames,BankName='bank8,bank15,bank16,bank45,bank49')
org1=CloneWorkspace(data1)
 
ApplyCalibration(data1,'CalibTable')



runs = [59293,59296]
filenames = '+'.join('/SNS/CORELLI/IPTS-{}/nexus/CORELLI_{}.nxs.h5'.format(ipts, r) for r in range(int(runs[0]), int(runs[1])+1))

data2=Load(filenames,BankName='bank54,bank57,bank73,bank74,bank80')
org2=CloneWorkspace(data2)
 
ApplyCalibration(data2,'CalibTable')
