from mantid.simpleapi import *
import numpy as np

corelli=LoadEmptyInstrument(InstrumentName='CORELLI')
inst=corelli.getInstrument()

centers=np.loadtxt('centers')

a=(2*25.4+2)/1000
y=np.arange(-7.5*a,8.5*a,a)

for row in centers:
    bank=int(row[1])
    tube=int(row[2])
    x = row[3:]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y)[0]
    #print(bank,tube,m, c,m*255)
    bank_pos = inst.getComponentByName('bank'+str(bank)+'/sixteenpack').getPos()
    for p in range(256):
        detID = (bank-1)*256*16+(tube-1)*256+p
        det_pos = inst.getDetector(detID).getPos()
        new_y = bank_pos[1] + p*m + c
        new_pos = [det_pos[0], new_y, det_pos[2]]
        print '{},{}'.format(detID, new_pos)
