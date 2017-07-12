#!/usr/bin/env python2
# ./run.py 47301 33 output.txt

from mantid.simpleapi import Load, Integration, LoadEmptyInstrument
import subprocess
import sys
import numpy as np

run = sys.argv[1]
bank = int(sys.argv[2])
height = int(sys.argv[3])
output = sys.argv[4]

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
inst = corelli.getInstrument()
bank_pos = inst.getComponentByName('bank'+str(bank)+'/sixteenpack').getPos()

a = (2*25.4+2)/1000
y = np.arange(-7.5*a, 8.5*a, a)

data = Load('CORELLI_'+str(run), BankName='bank'+str(bank))
data = Integration(data)
data_Y = data.extractY()*-1


def make_fityk_cmd(run, bank, tube):
    fityk_cmd = """@0 < 'COR_{0}_{1}_{2}.txt'
@0: A = a and not (-1 < x and x < 12.5)
@0: A = a and not (242.5 < x and x < 256)
F += Lorentzian(height={3}, center=~15.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~30.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~45.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~61.5, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~75.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~90.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~104.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~120.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~135.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~150.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~165.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~180.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~195.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~210.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~225.0, hwhm=~1.28083)
F += Lorentzian(height={3}, center=~240.0, hwhm=~1.28083)
$_hwhm = ~1.28083
%*.hwhm = $_hwhm
@0: guess Quadratic
@0: fit
%*.height = ~{3}
@0: fit
@0: info peaks > 'COR_{0}_{1}_{2}.peaks'
""".format(run, bank, tube+1, height)
    return fityk_cmd


f = open(output, 'a')


for tube in range(16):
    filename = 'COR_{}_{}_{}'.format(run, bank, tube+1)
    np.savetxt(filename+'.txt',
               np.concatenate((np.array(range(256), ndmin=2).T,
                               data_Y[range(256*tube, 256*(tube+1))]), axis=1))
    p = subprocess.Popen(['/usr/bin/cfityk', '-n'], stdin=subprocess.PIPE)
    p.communicate(make_fityk_cmd(run, bank, tube))
    centers = np.genfromtxt(filename+'.peaks', skip_header=1,
                            skip_footer=1, usecols=2)
    if (centers < 10).any() or (centers > 250).any():
        continue
    A = np.vstack([centers, np.ones(len(centers))]).T
    m, c = np.linalg.lstsq(A, y)[0]
    for pixel in range(256):
        detID = (bank-1)*256*16+(tube)*256+pixel
        det_pos = inst.getDetector(detID).getPos()
        new_y = bank_pos[1] + pixel*m + c
        new_pos = [det_pos[0], new_y, det_pos[2]]
        f.write('{},{}\n'.format(detID, new_pos))

f.close()
