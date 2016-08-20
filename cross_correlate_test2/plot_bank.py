#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

total = np.zeros((341,1667))
for bank in range(31,62):
    results = np.zeros((341,1667))
    for run in range(30338,30342):
        filename = 'CORELLI_'+str(run)+'_results_events_bank'+str(bank)+'.npy'
        temp=np.load(filename)
        results += temp
        total += temp
    y,x = results.shape
    xx=np.array(range(x))*10
    yy=np.array(range(y))*10
    X,Y = np.meshgrid(xx,yy)
    fig = plt.figure(figsize=(10,6))
    plt.pcolormesh(X, Y, results, vmin=0, vmax=1000)
    plt.title('bank'+str(bank))
    plt.xlabel('total time of flight (uS)')
    plt.ylabel('incident fliught time (uS)')
    plt.savefig('results_events_bank'+str(bank)+'.png')

fig = plt.figure(figsize=(10,6))
plt.pcolormesh(X, Y, total, vmin=0, vmax=10000)
plt.title('all banks')
plt.xlabel('total time of flight (uS)')
plt.ylabel('incident fliught time (uS)')
plt.savefig('results_events_all_bank.png')
