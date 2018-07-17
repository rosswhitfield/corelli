import matplotlib.pyplot as plt
import h5py
import numpy as np

cal_org = np.loadtxt('difc_org.txt')
cal_aligned = np.loadtxt('difc_aligned.txt')
cal_aligned2 = np.loadtxt('difc_aligned2.txt')
cal_aligned3 = np.loadtxt('difc_aligned3.txt')

with h5py.File('cal.h5', 'r') as f:
    cal1= f['calibration/difc'].value

with h5py.File('cal2.h5', 'r') as f:
    cal2= f['calibration/difc'].value

with h5py.File('cal3.h5', 'r') as f:
    cal3= f['calibration/difc'].value

with h5py.File('cal4.h5', 'r') as f:
    cal4= f['calibration/difc'].value


plt.plot(cal1/cal_org,label='cal1')
plt.plot(cal2/cal_aligned,label='cal2')
plt.plot(cal3/cal_aligned2,label='cal3')
plt.plot(cal4/cal_aligned3,label='cal4')
plt.legend()
plt.show()


plt.plot(cal1/cal_org,label='cal1')
plt.plot(cal2/cal1,label='cal2')
plt.plot(cal3/cal2,label='cal3')
plt.plot(cal4/cal3,label='cal4')
plt.legend()
plt.show()
