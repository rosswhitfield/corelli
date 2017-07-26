import numpy as np

a = (2*25.4+2)/1000
y = np.arange(-7.5*a, 8.5*a, a)

ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])

a_max=0
s=None

for run, banks, height in ws_list:
    banks = np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    bank_names = ','.join('bank'+str(b) for b in banks)
    print(run)
    print(banks)
    print('CORELLI_'+run)
    for bank in banks:
        for tube in range(16):
            filename = 'COR_{}_{}_{}'.format(run, bank, tube+1)
            centers = np.genfromtxt(filename+'.peaks', skip_header=1,
                                    skip_footer=1, usecols=2)
            if (centers < 10).any() or (centers > 250).any():
                print("skipping run {}, bank {}, tube {}".format(run, bank, tube))
                continue
            z = np.polyfit(centers, y, 2)
            poly = np.poly1d(z)
            print(z)
            print(poly)
            if np.abs(z[0]) > a_max:
                a_max=np.abs(z[0])
                s2=s
                s=poly

print(s)
print(s2)
