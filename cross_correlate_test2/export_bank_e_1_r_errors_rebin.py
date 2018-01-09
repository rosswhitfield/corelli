#!/usr/bin/env python
import numpy as np

total = np.zeros((341,16667))
error = np.zeros(16667)
for bank in range(31,62):
    results = np.zeros((341,16667))
    for run in range(30338,30346):
        filename = 'CORELLI_'+str(run)+'_results_events_b1_bank_r2.584_'+str(bank)+'.npy'
        temp=np.load(filename)
        results += temp
        total += temp
        filename = 'CORELLI_'+str(run)+'_results_events_b1_bank_r2.584_errorSq_'+str(bank)+'.npy'
        temp=np.load(filename)
        error += temp

y,x = results.shape
xx=np.array(range(x))*1
        

L1=20.0
L2=2.583
Lmc=17.999347
chopper_per = 3408.28925864
m=1.674927351e-27

# 1D define Ei

for mev, offset, x_offset in [(12,45,-0.05), (15,45,0.03), (20,45,-0.18), (25,40,-0.3), (30,40,-0.26), (50,50,0.03), (75,50,0.3)]:
    print(mev,offset)    
    ei = mev/1e3 * 1.602e-19
    vi = np.sqrt(2*ei/m)
    ti = Lmc/vi
    y = ti*1e6%chopper_per
    tof = (L1+L2)/vi
    xi = int(tof*1e6)
    t1 = L1/vi
    ix = range(xi-1000,xi+1000)
    t2 = xx[ix]/1e6 - t1
    v2 = L2/t2
    ef = 0.5*m*v2**2
    dEs = (ef-ei)/1.602e-19*1000 - x_offset
    ints = total[int((y-offset)/10),ix]
    e = np.sqrt(error[ix])
    np.savetxt("Ei_"+str(mev)+"_meV.xye",np.array([dEs,ints,e]).T)
    dEs = (dEs[::2]+dEs[1::2])/2
    ints = ints[::2]+ints[1::2]
    e_tmp = error[ix]
    e = np.sqrt(e_tmp[::2]+e_tmp[1::2])
    np.savetxt("Ei_"+str(mev)+"_meV_x2.xye",np.array([dEs,ints,e]).T)
    dEs = (dEs[::2]+dEs[1::2])/2
    ints = ints[::2]+ints[1::2]
    e_tmp = error[ix]
    e = np.sqrt(e_tmp[::4]+e_tmp[1::4]+e_tmp[2::4]+e_tmp[3::4])
    np.savetxt("Ei_"+str(mev)+"_meV_x4.xye",np.array([dEs,ints,e]).T)
