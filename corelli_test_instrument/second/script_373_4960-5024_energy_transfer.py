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
#elastic = np.zeros(5000)
energy_transfer = np.zeros(1001)

r=23.2868/26.06591 #26.20091
#f=(x*r)%8112
s=6e7/7393/255
m=1.674927351e-27
e=1.6e-19
sss=m*0.5/e

count=0
point=0
for n in xrange(size):
    a=f.read(8)
    (tof,pid) = unpack('ii',a)
    #if pid > 4960 and pid < 5024:
    if pid == 4992:
        count += 1
        if count%10000==0:
            print count, pid
        tof = tof/10.-52.
        while (n>=event_index[point]):
            point+=1
        #out[(chopper[point-1]-590.)/10.,tof/10.]+=1
        spectrum[tof/10]+=1
        c=chopper[point-1]-590.
        #elastic[tof/10]+=fact1
        #i=tof*r
        for i in range(2000,40000,100):
            ei=(23.2868/i*1e6)**2*sss
            ef=(2.00098/(tof-i*24.19993/23.2868)*1e6)**2*sss #2.00098 1.85098
            ij=int(((i-c)/s)%255)
            if ij in choppersequence:
                fact1 = 0.5
            else:
                fact1 = -0.5
            #print n,count,tof,c,i,ei,ef,ef-ei,ij,fact1
            de=ef-ei
            if abs(de)<0.025:
                energy_transfer[de*2e4+500]+=fact1


f.close()


np.save('energy_transfer4',energy_transfer)

x=np.linspace(-25,25,1001)
plt.plot(x,energy_transfer)
plt.show()
