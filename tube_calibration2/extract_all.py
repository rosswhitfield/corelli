from mantid.simpleapi import Load, Integration
import numpy as np

ipts=18479

ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration2/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])

for run, banks, height in ws_list:
    banks = np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    bank_names = ','.join('bank'+str(b) for b in banks)
    print(run)
    print(banks)
    print('CORELLI_'+run)
    runs = run.split('-')
    filenames = '+'.join('/SNS/CORELLI/IPTS-{}/nexus/CORELLI_{}.nxs.h5'.format(ipts, r) for r in range(int(runs[0]), int(runs[1])+1))
    for bank in banks:
        data = Load(Filename=filenames, BankName='bank'+str(bank))
        data = Integration(data)
        data_Y = data.extractY()*-1
        for tube in range(16):
            filename = 'COR_{}_{}_{}'.format(run, bank, tube+1)
            np.savetxt(filename+'.txt',
                       np.concatenate((np.array(range(256), ndmin=2).T,
                                       data_Y[range(256*tube, 256*(tube+1))]), axis=1))

