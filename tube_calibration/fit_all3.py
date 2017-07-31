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
$a = ~0.0
$b = ~282.0
$c = ~128.0
F += Lorentzian(height={3}, center=0.396*0.396*$a-0.396*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.3432*0.3432*$a-0.3432*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.2904*0.2904*$a-0.2904*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.2376*0.2376*$a-0.2376*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.1848*0.1848*$a-0.1848*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.132*0.132*$a-0.132*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.0792*0.0792*$a-0.0792*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.0264*0.0264*$a-0.0264*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.0264*0.0264*$a+0.0264*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.0792*0.0792*$a+0.0792*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.132*0.132*$a+0.132*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.1848*0.1848*$a+0.1848*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.2376*0.2376*$a+0.2376*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.2904*0.2904*$a+0.2904*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.3432*0.3432*$a+0.3432*$b+$c, hwhm=~1.28083)
F += Lorentzian(height={3}, center=0.396*0.396*$a+0.396*$b+$c, hwhm=~1.28083)
$_hwhm = ~1.28083
%*.hwhm = $_hwhm
@0: guess Quadratic
@0: fit
%*.height = ~{3}
@0: fit
info $a > 'COR_{0}_{1}_{2}.param3'
info $b >> 'COR_{0}_{1}_{2}.param3'
info $c >> 'COR_{0}_{1}_{2}.param3'
""".format(run, bank, tube+1, height)
    return fityk_cmd


ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])

f = open(output, 'a')

def solve_quad(param, x):
    a, b, c = param
    cx = c-x
    if np.abs(a) < 1e-5:
        return (-cx)/b
    else:
        d = b**2-4*a*cx
        return (-b+np.sqrt(d))/(2*a) #,(-b-np.sqrt(d))/(2*a)
            


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
            param = np.genfromtxt(filename+'.param3', usecols=4)
            if np.abs(param[0]) > 50 or param[1] < 270 or np.abs(param[2]-127) > 5:
                continue            
            for pixel in range(256):
                detID = (bank-1)*256*16+(tube)*256+pixel
                det_pos = inst.getDetector(detID).getPos()
                new_y = bank_pos[1] + solve_quad(param,pixel)
                new_pos = [det_pos[0], new_y, det_pos[2]]
                f.write('{},{}\n'.format(detID, new_pos))

f.close()
