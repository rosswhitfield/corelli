#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

total = np.zeros((341,1667))
for bank in range(31,62):
    results = np.zeros((341,1667))
    for run in range(30338,30346):
        filename = 'CORELLI_'+str(run)+'_results_events_bank'+str(bank)+'.npy'
        temp=np.load(filename)
        results += temp
        total += temp
    y,x = results.shape
    xx=np.array(range(x))*10
    yy=np.array(range(y))*10
    X,Y = np.meshgrid(xx,yy)
    fig = plt.figure(figsize=(12,6))
    plt.pcolormesh(X, Y, results, vmin=0, vmax=2000)
    #plt.pcolormesh(X, Y, results)
    plt.colorbar()
    plt.title('bank'+str(bank))
    plt.xlabel('total time of flight (uS)')
    plt.ylabel('incident fliught time (uS)')
    plt.savefig('results_events_bank'+str(bank)+'.png')

fig = plt.figure(figsize=(12,6))
plt.pcolormesh(X, Y, total, vmin=0, vmax=50000)
#plt.pcolormesh(X, Y, total)
plt.colorbar()
plt.title('all banks')
plt.xlabel('total time of flight (uS)')
plt.ylabel('incident fliught time (uS)')
plt.savefig('results_events_all_bank.png')


L1=20.0
L2=2.585

# +4meV                                                                        
#de=-0.004*1.6e-19
m=1.674927351e-27

#yyy=xx*Lmc/L
#xxx=yyy+yyy*Lcs/Lmc+Lsd/np.sqrt((Lmc/yyy*1e6)**2+2*de/m)*1e6

t1=xx*(L1/(L1+L2))
#t2=yy-t1
de=Y.copy()
for i in len(Y):
    t2=(Y[i]-xx)%3400+xx-t1
    de[i] = 0.5*m*((L2/t2)**2-(L1/t1)**2)
