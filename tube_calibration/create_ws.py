from mantid.simpleapi import Load, MaskBTP, InvertMask, mtd, CloneWorkspace, Integration
import numpy as np
ws_list=np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',delimiter=',',dtype=[('runs','|S11'),('banks','5i8'),('height','i8')])

for run, banks, height in ws_list:
    banks=np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    data = Load(Filename='CORELLI_'+run)
    data = Integration(data)
    MaskBTP(data,Bank=','.join(str(b) for b in banks))
    if 'accum' in mtd:
        accum += data
    else:
        accum=CloneWorkspace(data)

