import numpy as np
import matplotlib.pyplot as plt

banks = [8,15,16,45,49,54,57,73,74,80]

map1 = {8:'47316', 15:'47313', 16:'47313', 45:'47316', 49:'47312', 54:'47310', 57:'47326', 73:'47322', 74:'47322', 80:'47323'}
map2 = {8:'59288-59291', 15:'59288-59291', 16:'59288-59291', 45:'59288-59291', 49:'59288-59291', 54:'59293-59296', 57:'59293-59296', 73:'59293-59296', 74:'59293-59296', 80:'59293-59296'}


for bank in banks:
    f, axarr = plt.subplots(4,4,figsize=(20,20))
    for i in range(4):
        for j in range(4):
            tube = i+4*j+1
            old = np.genfromtxt('../tube_calibration/COR_{}_{}_{}.txt'.format(map1[bank],bank,tube))
            new = np.genfromtxt('COR_{}_{}_{}.txt'.format(map2[bank],bank,tube))
            new[:,1] *= old[:,1].min()/new[:,1].min()
            #new[:,1] *= 2
            axarr[i, j].plot(old[:,0], old[:,1])
            axarr[i, j].plot(new[:,0], new[:,1])
            axarr[i, j].set_title('bank{}'.format(bank))
    f.savefig('COR_{}_compare.png'.format(bank))
