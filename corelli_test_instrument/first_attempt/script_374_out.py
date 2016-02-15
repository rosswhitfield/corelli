import numpy as np
from pylab import *
from struct import *
import os
import math
#from mantid.simpleapi import *

das_file="/home/rwp/corelli/corelli/DAS_374/DAS_374"
chopper_file ="/home/rwp/corelli/corelli/timingdata/chopper_374_3.dat"
pulse_file   ="/home/rwp/corelli/corelli/timingdata/rtdl_374_3.dat"
choppersequence_file = "/home/rwp/corelli/corelli/choppersequence255.txt"

f=open(choppersequence_file)
choppersequence = f.readlines() # listed is open/non-absorbing
choppersequence = map(int,choppersequence)
f.close()

dt = np.dtype([('nanoseconds',np.uint32),('seconds',np.uint32),('event_index',np.uint64),('pCurrent',np.float64)])
pulses = np.fromfile(das_file+"_pulseid.dat",dtype=dt) 

chopper = np.fromfile(chopper_file,dtype=np.float)
rtdl_pulses = np.fromfile(pulse_file,dtype=(np.uint32,6))

out = np.zeros((812,5000))
#results = np.zeros((5000,5000))

#events = np.load('events_374_4992.npy')
events = np.load('events_374_4960-5024.npy')
print 'Events =',len(events)


event_index=pulses['event_index']

i=0
for n in xrange(len(events)):
    if n%10000==0:
        print n
    while (events[n,1]>event_index[i]):
        i+=1
    #print n,i,events[n],event_index[i],chopper[i-1]
    out[(chopper[i-1]-590.)/10.,(events[n,0]/10.-52.)/10.]+=1


np.save('out_374_4960-5024',out)


x=linspace(0, 50000, 5000)
y=linspace(0, 8120, 812)
X,Y = meshgrid(x,y)

fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, out)
cb = fig.colorbar(p, ax=ax)
fig.show()

s=6e6/7393/255

results = np.zeros((812,5000))
for i in range(812):
    print 'i =',i
    for j in range(812):
        ij = int(((i-j)/s)%255)
        if ij in choppersequence:
            fact1 = 0.5
        else:
            fact1 = -0.5
        for k in xrange(5000):
            results[i,k]+=fact1*out[j,k]


np.save('results_374_4960-5024',results)
#results /=64

fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=5000)
cb = fig.colorbar(p, ax=ax)
fig.show()

