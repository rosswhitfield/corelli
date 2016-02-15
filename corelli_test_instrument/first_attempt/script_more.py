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

#events = LoadEventPreNexus(das_file+"_neutron_event.dat",das_file+"_pulseid.dat")

#events = np.fromfile(das_file+"_neutron_event.dat",dtype=(np.uint32,2))
###len(events) = 728920238
###eventPixelID == 4992: 97004

dt = np.dtype([('nanoseconds',np.uint32),('seconds',np.uint32),('event_index',np.uint64),('pCurrent',np.float64)])
pulses = np.fromfile(das_file+"_pulseid.dat",dtype=dt) 

chopper = np.fromfile(chopper_file,dtype=np.float)
rtdl_pulses = np.fromfile(pulse_file,dtype=(np.uint32,6))

count = 0
f = open(das_file+"_neutron_event.dat")
f.seek(0,os.SEEK_END)
size = f.tell()/8
f.seek(0,os.SEEK_SET)
print 'Events =',size

out = np.zeros((812,5000))
#results = np.zeros((5000,5000))

for n in xrange(size):
    a=f.read(8)
    (tof,pid) = unpack('ii',a)
    if pid > 4960 and pid < 5024:
        count += 1
        #print count, pid
        tof = tof/10.-52.
        pulse = np.searchsorted(pulses['event_index'],n+1)-1
        #print tof,pulse,chopper[pulse]-590.
        #j = int(chopper[pulse]-590.)%256
        out[(chopper[pulse]-590.)/10.,tof/10.]+=1

f.close()
print 'Count =',count

np.save('out_373_4960-5024',out)

x=linspace(0, 50000, 5000)
y=linspace(0, 8120, 812)
X,Y = meshgrid(x,y)

#fig, ax = plt.subplots()
#p = ax.pcolormesh(X, Y, out, vmax=5)
#cb = fig.colorbar(p, ax=ax)
#fig.show()

s=6e6/7393/256

results = np.zeros((812,5000))
for i in range(812):
    print 'i =',i
    for j in range(812):
        ij = int(((i-j)/s)%256)
        if ij in choppersequence:
            fact1 = 0.5
        else:
            fact1 = -0.5
        for k in range(5000):
            results[i,k]+=fact1*out[j,k]

np.save('results_373_4960-5024',results)
results /=64

#fig, ax = plt.subplots()
#p = ax.pcolormesh(X, Y, results, vmin=0, vmax=5)
#cb = fig.colorbar(p, ax=ax)
#fig.show()

