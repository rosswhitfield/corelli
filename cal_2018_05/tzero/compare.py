import matplotlib.pyplot as plt
import h5py
import numpy as np

cal_org = np.loadtxt('../a/difc_org.txt')

with h5py.File('cal.h5', 'r') as f:
    cal_t0= f['calibration/difc'].value

with h5py.File('../a/cal.h5', 'r') as f:
    cal= f['calibration/difc'].value

plt.plot(cal/cal_org,label='cal')
plt.plot(cal_t0/cal_org,label='cal_t0')
plt.legend()
plt.show()
