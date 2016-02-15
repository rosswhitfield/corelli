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
l=len(event_index)

events = np.load('events_373_4992.npy')

spectrum = np.zeros(5000)
elastic = np.zeros(5000)

s=6e7/7393/255
m=1.674927351e-27
e=1.6e-19
sss=m*0.5/e
r=23.2868/26.06591 #26.20091

lmc=23.2868
lcs=0.91313
lsd=2.40098 #2.00098

#tof = i + j + k
#i+j = i*(lmc + lcs)/lmc
#k = tof - i*(lmc + lcs)/lmc

#ei = (lmc/i*1e6)**2*sss
#ef = (lsd/k)**2*sss
#ef = ( lsd/(tof - i*(lmc + lcs)/lmc)*1e6 )**2*sss
#de = ef - ei
#de = (lsd/(tof - i*(lmc + lcs)/lmc)*1e6 )**2*sss - (lmc/i*1e6)**2*sss


#elastic
#tof = i   * (lmc+lcs+lsd)/lmc
#i   = tof * lmc/(lmc+lcs+lsd)

delta_e=0

point=0
for n in xrange(len(events)):
    if n%10000==0:
        print n
    while (events[n,1]>=event_index[point]):
        point+=1
    tof = events[n,0]/10.-52.
    spectrum[tof/10]+=1
    c=chopper[point-1]-590.
    i=tof*lmc/(lmc+lcs+lsd)
    ij=int(((i-c)/s)%255)
    if ij in choppersequence:
        fact1 = 0.5
    else:
        fact1 = -0.5
    elastic[tof/10]+=fact1

x=np.linspace(0,50000,5000)

fig, ax = plt.subplots()
p1 = plt.plot(x,spectrum, label="Total")
p2 = plt.plot(x,elastic, label="Elastic")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
fig.show()
