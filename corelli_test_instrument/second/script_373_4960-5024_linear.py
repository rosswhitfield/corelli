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

#out = np.zeros((812,5000))
spectrum = np.zeros(5000)
elastic = np.zeros(5000)

r=23.2868/26.05091 #26.20091
#f=(x*r)%8112
s=6e7/7393/255


count=0
point=0
for n in xrange(size):
    a=f.read(8)
    (tof,pid) = unpack('ii',a)
    if pid > 4960 and pid < 5024:
        count += 1
        if count%10000==0:
            print count, pid
        tof = tof/10.-52.
        while (n>=event_index[point]):
            point+=1
        #out[(chopper[point-1]-590.)/10.,tof/10.]+=1
        spectrum[tof/10]+=1
        c=chopper[point-1]-590.
        i=tof*r
        ij=int(((i-c)/s)%255)
        if ij in choppersequence:
            fact1 = 0.5
        else:
            fact1 = -0.5
        elastic[tof/10]+=fact1

f.close()

x=np.linspace(0, 50000, 5000)
plt.plot(x,spectrum)
plt.plot(x,elastic*4.5)
plt.show()


