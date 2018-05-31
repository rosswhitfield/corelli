import numpy as np
import matplotlib.pyplot as plt

difc = np.loadtxt('difc.txt')
difc_org = np.loadtxt('difc_org.txt')
cal = np.loadtxt('cal_difc.txt')

plt.plot(difc)
plt.plot(cal)
plt.show()

plt.plot(difc/difc_org)
plt.show()


plt.plot(cal/difc)
plt.show()
