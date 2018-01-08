#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(12,6))
total = np.zeros((341,16667))
for bank in range(31,62):
    results = np.zeros((341,16667))
    for run in range(30338,30346):
        filename = 'CORELLI_'+str(run)+'_results_events_b1_bank'+str(bank)+'.npy'
        temp=np.load(filename)
        results += temp
        total += temp
    y,x = results.shape
    xx=np.array(range(x))*1
    yy=np.array(range(y))*10
    X,Y = np.meshgrid(xx,yy)
    plt.clf()
    plt.pcolormesh(X, Y, results, vmin=0, vmax=100,cmap='viridis')
    #plt.pcolormesh(X, Y, results)
    plt.colorbar()
    plt.title('bank'+str(bank))
    plt.xlabel('total time of flight (uS)')
    plt.ylabel('incident flight time (uS)')
    plt.savefig('results_events_bank'+str(bank)+'_viridis.png')

plt.clf()
plt.pcolormesh(X, Y, total, vmin=200, vmax=1000, cmap='Greys')
#plt.pcolormesh(X, Y, total)
plt.colorbar()
plt.title('all banks')
plt.xlabel('total time of flight (uS)')
plt.ylabel('incident flight time (uS)')
plt.savefig('results_events_all_bank_viridis.png')

