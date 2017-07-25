from mantid.simpleapi import Load, Integration, LoadEmptyInstrument, mtd, CloneWorkspace
import subprocess
import sys
import numpy as np

output = sys.argv[1]

corelli = LoadEmptyInstrument(InstrumentName='CORELLI')
inst = corelli.getInstrument()

a = (2*25.4+2)/1000
y = np.arange(-7.5*a, 8.5*a, a)

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


ws_list=np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',delimiter=',',dtype=[('runs','|S11'),('banks','5i8'),('height','i8')])

f = open(output, 'a')


for run, banks, height in ws_list:
    banks=np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    bank_names=','.join('bank'+str(b) for b in banks)
    print(run)
    print(banks)
    print('CORELLI_'+run)
    for bank in banks:
        bank_pos = inst.getComponentByName('bank'+str(bank)+'/sixteenpack').getPos()
        data = Load(Filename='CORELLI_'+run, BankName='bank'+str(bank))
        data = Integration(data)
        data_Y = data.extractY()*-1

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
                print("skipping run {}, bank {}, tube {}".format(run,bank,tube))
                continue
            z = np.polyfit(centers, y, 2)
            poly = np.poly1d(z)
            for pixel in range(256):
                detID = (bank-1)*256*16+(tube)*256+pixel
                det_pos = inst.getDetector(detID).getPos()
                new_y = bank_pos[1] + poly(pixel)
                new_pos = [det_pos[0], new_y, det_pos[2]]
                f.write('{},{}\n'.format(detID, new_pos))

f.close()

                                                                                                            
