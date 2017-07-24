from mantid.simpleapi import Load, Integration, LoadEmptyInstrument
import numpy as np

ws_list=np.genfromtxt('list',delimiter=',',dtype=int)

accum = LoadEmptyInstrument(InstrumentName='CORELLI')

for run, *banks in ws_list:
    banks=np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    banks=','.join('bank'+str(b) for b in banks)
    print(run)
    print(banks)
    data = Load('CORELLI_'+str(run), BankName=banks)
    data = Integration(data)
    accum =+ data
