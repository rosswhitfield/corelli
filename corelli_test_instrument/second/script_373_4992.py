import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from struct import *
import os
import math

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

event_index=pulses['event_index']

f = open(das_file+"_neutron_event.dat")
f.seek(0,os.SEEK_END)
size = f.tell()/8
f.seek(0,os.SEEK_SET)
print 'Events =',size

out = np.zeros((812,5000))

count=0
point=0
for n in xrange(size):
    a=f.read(8)
    (tof,pid) = unpack('ii',a)
    if pid == 4992:
        count += 1
        if count%10000==0:
            print count, pid
        tof = tof/10.-52.
        while (n>=event_index[point]):
            point+=1
        out[(chopper[point-1]-590.)/10.,tof/10.]+=1

f.close()

np.save('out_373_4992',out)

x=np.linspace(0, 50000, 5000)
y=np.linspace(0, 8120, 812)
X,Y = np.meshgrid(x,y)

fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, out)
cb = fig.colorbar(p, ax=ax)
#fig.show()
fig.savefig('out_373_4992.png')

s=6e6/7393/255
m=len(choppersequence)
N=255
c=(m-1.)/(N-1.)

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

results /= (m*(1-c))
np.save('results_373_4992',results)


fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0)
cb = fig.colorbar(p, ax=ax)
#fig.show()
fig.savefig('results_373_4992.png')

