import matplotlib.pyplot as plt
import numpy as np

ws_list = np.genfromtxt('/SNS/users/rwp/corelli/tube_calibration/list',
                        delimiter=',',
                        dtype=[('runs', '|S11'), ('banks', '5i8'), ('height', 'i8')])


for run, banks, height in ws_list:
    banks = np.asarray(banks)
    banks = banks[np.nonzero(banks)]
    for bank in banks:
        plt.clf()
        for tube in range(16):
            filename = 'COR_{}_{}_{}'.format(run, bank, tube+1)
            xy = np.loadtxt(filename+'.txt')
            plt.plot(xy[:, 0], xy[:, 1], label=filename)
        plt.legend()
        plt.show()
