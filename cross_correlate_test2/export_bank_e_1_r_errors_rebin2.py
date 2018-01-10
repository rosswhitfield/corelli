#!/usr/bin/env python
import numpy as np

total = np.zeros((341,16667))
error = np.zeros(16667)
for bank in range(31,62):
    for run in range(30338,30346):
        filename = 'CORELLI_'+str(run)+'_results_events_b1_bank_r2.584_'+str(bank)+'.npy'
        temp=np.load(filename)
        total += temp
        filename = 'CORELLI_'+str(run)+'_results_events_b1_bank_r2.584_errorSq_'+str(bank)+'.npy'
        temp=np.load(filename)
        error += temp


total = total[:,:15120]
error = error[:15120]

y,x = total.shape
xx=np.array(range(x))*1
        

L1=20.0
L2=2.583
Lmc=17.999347
chopper_per = 3408.28925864
m=1.674927351e-27

# 1D define Ei

for bin_size in range(1,21):
    if bin_size in (11, 13, 17, 19):
        continue
    error_tmp = error.reshape(-1, bin_size).sum(axis=1)
    total_tmp = total.reshape((341, -1, bin_size)).sum(axis=2)
    xx_tmp = np.average(xx.reshape(-1, bin_size), axis=1)
    for mev, offset, x_offset in [(12,45,0.05)]: #, (15,45,-0.03), (20,45,0.18), (25,40,0.3), (30,40,0.26), (50,50,-0.03), (75,50,-0.3)]:
        print(mev,offset)    
        ei = mev/1e3 * 1.602e-19
        vi = np.sqrt(2*ei/m)
        ti = Lmc/vi
        y = ti*1e6%chopper_per
        tof = (L1+L2)/vi
        xi = int(tof*1e6/bin_size)
        t1 = L1/vi
        t2 = xx_tmp/1e6 - t1
        v2 = L2/t2
        ef = 0.5*m*v2**2
        dEs = (ei-ef)/1.602e-19*1000 - x_offset
        ints = total_tmp[int((y-offset)/10),:]
        e = np.sqrt(error_tmp)
        mask = np.logical_and(np.abs(dEs) < 10, np.abs(xx_tmp - xx_tmp[xi]) < 1000)
        np.savetxt("Ei_"+str(mev)+"_meV_"+str(bin_size)+"us.xye",np.array([dEs[mask],ints[mask],e[mask]]).T)
