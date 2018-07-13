"""
P=(B x + C)/(A x + 1)

"""

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
@0: A = a and not (240.5 < x and x < 256)
$a = 0.0
$b = 282.0
$c = ~127.0
F += Lorentzian(height={3}, center=(-0.396*$b+$c)/(-0.396*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.3432*$b+$c)/(-0.3432*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.2904*$b+$c)/(-0.2904*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.2376*$b+$c)/(-0.2376*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.1848*$b+$c)/(-0.1848*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.132*$b+$c)/(-0.132*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.0792*$b+$c)/(-0.0792*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(-0.0264*$b+$c)/(-0.0264*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.0264*$b+$c)/(0.0264*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.0792*$b+$c)/(0.0792*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.132*$b+$c)/(0.132*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.1848*$b+$c)/(0.1848*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.2376*$b+$c)/(0.2376*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.2904*$b+$c)/(0.2904*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.3432*$b+$c)/(0.3432*$a+1), hwhm=~1.28083)
F += Lorentzian(height={3}, center=(0.396*$b+$c)/(0.396*$a+1), hwhm=~1.28083)
$_hwhm = 1.28083
%*.hwhm = $_hwhm
@0: guess Quadratic
@0: fit
$_hwhm = ~1.28083
%*.hwhm = $_hwhm
@0: fit
$a = ~0.0
$b = ~282.0
@0: fit
%*.height = ~{3}
@0: fit
info $a > 'COR_{0}_{1}_{2}.param4'
info $b >> 'COR_{0}_{1}_{2}.param4'
info $c >> 'COR_{0}_{1}_{2}.param4'
""".format(run, bank, tube+1, height)
    return fityk_cmd


ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration2/57_80/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])

def solve(param, x):
    a, b, c = param
    return (c-x)/(a*x-b)

run, banks, height = ws_list.item(0)
#run = run.decode()

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
        #p = subprocess.Popen(['/usr/bin/cfityk', '-n'], stdin=subprocess.PIPE)
        np.savetxt(filename+'.fit', [make_fityk_cmd(run, bank, tube)], fmt='%s')
