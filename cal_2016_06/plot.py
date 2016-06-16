import matplotlib.pyplot as plt
import numpy as np
C60 = np.loadtxt('cal_C60_20501-8_sum4_mask_lt_3_MaxChiSq3.cal')[3:,1:3]
Si = np.loadtxt('cal_Si_20492-9_sum4_mask_lt_3_MaxChiSq3.cal')[3:,1:3]
Diamond = np.loadtxt('cal_Diamond_20482-9_sum4_mask_lt_3.cal')[3:,1:3]

Si[:,1][Si[:,1]==0] = np.nan
C60[:,1][C60[:,1]==0] = np.nan
Diamond[:,1][Diamond[:,1]==0] = np.nan

plt.plot(Si[:,0], Si[:,1], label='Silicon')
plt.plot(C60[:,0], C60[:,1], label='C60')
plt.plot(Diamond[:,0], Diamond[:,1], label='Diamond')

plt.legend()
plt.show()


C60_old = np.loadtxt('../cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal')[3:,1:3]
Si_old = np.loadtxt('../cal_2016_02/cal_Si_20492-9_sum4_mask_lt_3.cal')[3:,1:3]
Diamond_old = np.loadtxt('../cal_2016_02/cal_Diamond_20482-9_sum4_mask_lt_3.cal')[3:,1:3]

Si_old[:,1][Si_old[:,1]==0] = np.nan
C60_old[:,1][C60_old[:,1]==0] = np.nan
Diamond_old[:,1][Diamond_old[:,1]==0] = np.nan

plt.plot(Si_old[:,0], Si_old[:,1], label='Silicon_old')
plt.plot(C60_old[:,0], C60_old[:,1], label='C60_old')
plt.plot(Diamond_old[:,0], Diamond_old[:,1], label='Diamond_old')
