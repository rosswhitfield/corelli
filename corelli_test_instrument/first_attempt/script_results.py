import numpy as np
from pylab import *
from struct import *
import os
import math
#from mantid.simpleapi import *

das_file="/home/rwp/corelli/corelli/DAS_373/DAS_373"
chopper_file ="/home/rwp/corelli/corelli/timingdata/chopper_373_2.dat"
pulse_file   ="/home/rwp/corelli/corelli/timingdata/rtdl_373_2.dat"
choppersequence_file = "/home/rwp/corelli/corelli/choppersequence255.txt"

f=open(choppersequence_file)
choppersequence = f.readlines() # listed is open/non-absorbing
choppersequence = map(int,choppersequence)
f.close()

dt = np.dtype([('nanoseconds',np.uint32),('seconds',np.uint32),('event_index',np.uint64),('pCurrent',np.float64)])
pulses = np.fromfile(das_file+"_pulseid.dat",dtype=dt) 

chopper = np.fromfile(chopper_file,dtype=np.float)
rtdl_pulses = np.fromfile(pulse_file,dtype=(np.uint32,6))

#events = np.load('events_373_4992.npy')
#events = np.load('events_373_4960-5024.npy')
#print 'Events =',len(events)

event_index=pulses['event_index']

f = open(das_file+"_neutron_event.dat")
f.seek(0,os.SEEK_END)
size = f.tell()/8
f.seek(0,os.SEEK_SET)
print 'Events =',size

out = np.zeros((812,5000))
results = np.zeros((812,5000))

count=0
i=0
s=6e6/7393/255

for n in xrange(size):
    a=f.read(8)
    (tof,pid) = unpack('ii',a)
    if pid > 4960 and pid < 5024:
    #if pid/10 == 499:
        count += 1
        if count%10000==0:
            print count, pid
        tof = tof/10.-52.
        #pulse = np.searchsorted(pulses['event_index'],n+1)-1
        while (n>=event_index[i]):
            i+=1
        out[(chopper[i-1]-590.)/10.,tof/10.]+=1
        k=tof/10.
        j=(chopper[i-1]-590.)/10.
        for ii in range(812):
            iij = int(((ii-j)/s)%255)
            if iij in choppersequence:
                fact1 = 0.5
            else:
                fact1 = -0.5
            results[ii,k]+=fact1
        
f.close()

np.save('out_373_4960-5024_test_255',out)
np.save('results_373_4960-5024_test_255',results)


#x=linspace(0, 50000, 5000)
#y=linspace(0, 8120, 812)
#X,Y = meshgrid(x,y)

#fig, ax = plt.subplots()
#p = ax.pcolormesh(X, Y, out)
#cb = fig.colorbar(p, ax=ax)
#fig.show()


#for i in range(812):
#    print 'i =',i
#    for j in range(812):
#        ij = int(((i-j)/s)%256)
#        if ij in choppersequence:
#            fact1 = 0.5
#        else:
#            fact1 = -0.5
#        for k in xrange(5000):
#            results[i,k]+=fact1*out[j,k]

#np.save('results_373_4960-5024',results)
#results /=64

#fig, ax = plt.subplots()
#p = ax.pcolormesh(X, Y, results, vmin=0)
#cb = fig.colorbar(p, ax=ax)
#fig.show()

