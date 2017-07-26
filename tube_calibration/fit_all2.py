from mantid.simpleapi import LoadEmptyInstrument
import subprocess
import sys
import numpy as np

output = sys.argv[1]

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
inst = corelli.getInstrument()

def make_fityk_cmd(run, bank, tube):
    fityk_cmd = """@0 < 'COR_{0}_{1}_{2}.txt'
@0: A = a and not (-1 < x and x < 12.5)
@0: A = a and not (242.5 < x and x < 256)
$b = ~0.003535
$c = ~-0.45257
F += Lorentzian(height=2000, center=(-0.396-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(-0.3432-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(-0.2904-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(-0.2376-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(-0.1848-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(-0.132-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(-0.0792-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(-0.0264-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.0264-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.0792-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.132-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.1848-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.2376-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.2904-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.3432-$c)/$b, hwhm=~1.28083)
F += Lorentzian(height=2000, center=(0.396-$c)/$b, hwhm=~1.28083
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
info $b > 'COR_{0}_{1}_{2}.param'
info $c >> 'COR_{0}_{1}_{2}.param'
""".format(run, bank, tube+1, height)
    return fityk_cmd


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
            p = subprocess.Popen(['/usr/bin/cfityk', '-n'], stdin=subprocess.PIPE)
            p.communicate(make_fityk_cmd(run, bank, tube))
            param = np.genfromtxt(filename+'.param', usecols=4)
            if np.any(np.isnan(param)+np.isinf(param)+(np.abs(param) > 1)):
                continue
            for pixel in range(256):
                detID = (bank-1)*256*16+(tube)*256+pixel
                det_pos = inst.getDetector(detID).getPos()
                new_y = bank_pos[1] + pixel*param[0] + param[1]
                new_pos = [det_pos[0], new_y, det_pos[2]]
                f.write('{},{}\n'.format(detID, new_pos))

f.close()
