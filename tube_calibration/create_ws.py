from mantid.simpleapi import Load, Integration, LoadEmptyInstrument, mtd, CloneWorkspace
import numpy as np

ws_list=np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',delimiter=',',dtype=int)

for run, *banks in ws_list:
    banks=np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    banks=','.join('bank'+str(b) for b in banks)
    print(run)
    print(banks)
    data = Load('CORELLI_'+str(run), BankName=banks)
    data = Integration(data)
    if mtd.doesExist('accum'):
      accum+=data 
    else: 
      accum=CloneWorkspace(data)

