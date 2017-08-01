from __future__ import print_function
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
    for bank in banks:
        lengths=[]
        for tube in range(16):
            filename = 'COR_{}_{}_{}'.format(run, bank, tube+1)
            param = np.genfromtxt(filename+'.param3', usecols=4)
            if np.abs(param[0]) > 50 or param[1] < 270 or np.abs(param[2]-127) > 5:
                continue
            length = solve_quad(param,255) - solve_quad(param,0)
            lengths.append(length)
        #print(bank,np.min(lengths),np.max(lengths),np.median(lengths),np.mean(lengths))
        print(bank,np.median(lengths))
