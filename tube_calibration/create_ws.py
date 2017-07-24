from mantid.simpleapi import Load, Integration, LoadEmptyInstrument, mtd, CloneWorkspace
import subprocess
import sys
import numpy as np

output = sys.argv[1]

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
inst = corelli.getInstrument()
bank_pos = inst.getComponentByName('bank'+str(bank)+'/sixteenpack').getPos()

a = (2*25.4+2)/1000
y = np.arange(-7.5*a, 8.5*a, a)

ws_list=np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',delimiter=',',dtype=int)

for run, *banks, height in ws_list:
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

