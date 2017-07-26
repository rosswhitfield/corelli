from mantid.simpleapi import LoadEmptyInstrument
import subprocess
import sys
import numpy as np

output = sys.argv[1]

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
inst = corelli.getInstrument()

ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])

f = open(output, 'a')


for run, banks, height in ws_list:
    banks = np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    bank_names = ','.join('bank'+str(b) for b in banks)
    print(run)
    print(banks)
    print('CORELLI_'+run)
    for bank in banks:
        bank_pos = inst.getComponentByName('bank'+str(bank)+'/sixteenpack').getPos()
        for tube in range(16):
            filename = 'COR_{}_{}_{}'.format(run, bank, tube+1)
            param = np.genfromtxt(filename+'.param', usecols=4)
            for pixel in range(256):
                detID = (bank-1)*256*16+(tube)*256+pixel
                det_pos = inst.getDetector(detID).getPos()
                new_y = bank_pos[1] + pixel*param[0] + param[1]
                new_pos = [det_pos[0], new_y, det_pos[2]]
                f.write('{},{}\n'.format(detID, new_pos))

f.close()
