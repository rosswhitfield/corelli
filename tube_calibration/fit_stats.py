import numpy as np

ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])


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
