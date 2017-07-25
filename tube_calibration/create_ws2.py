from mantid.simpleapi import Load, mtd, CloneWorkspace, Integration, SaveNexus, RemoveLogs
import numpy as np

ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])

for run, banks, height in ws_list:
    banks = np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    bank_names = ','.join('bank'+str(b) for b in banks)
    data = Load(Filename='CORELLI_'+run, BankName=bank_names, SingleBankPixelsOnly=False)
    pc=sum(data.getRun()['proton_charge'].value)
    data = Integration(data)
    data/=pc
    RemoveLogs(data)
    if 'accum' in mtd:
        accum += data
    else:
        accum = CloneWorkspace(data)

SaveNexus(accum, '/SNS/users/rwp/corelli/tube_calibration/all_banks.nxs')
