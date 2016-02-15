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

events = np.load('events_373_4992.npy')

spectrum = np.zeros(5000)
#elastic = np.zeros(5000)
energy_transfer = np.zeros(100001)

#r=23.2868/26.06591 #26.20091
#f=(x*r)%8112
s=6e7/7393/255
m=1.674927351e-27
e=1.6e-19
ei_max=0
ef_max=0
sss=m*0.5/e

count=0
point=0
l=len(event_index)
for n in xrange(len(events)):
    if n%10000==0:
        print n
    while (events[n,1]>=event_index[point]):
        point+=1
    tof = events[n,0]/10.-52.
    spectrum[tof/10]+=1
    c=chopper[point-1]-590.
    for i in range(2000,40000,10):
        ei=(23.2868/i*1e6)**2*sss
        ef=(2.00098/(tof-i*24.19993/23.2868)*1e6)**2*sss #2.00098 1.85098
        if abs(ei)>abs(ei_max):
            ei_max=ei
        if abs(ef)>abs(ei_max):
            ef_max=ef
        ij=int(((i-c)/s)%255)
        if ij in choppersequence:
            fact1 = 0.5
        else:
            fact1 = -0.5
            #print n,count,tof,c,i,ei,ef,ef-ei,ij,fact1
        de=ef-ei
        if abs(de)<2.5:
            energy_transfer[de*2e4+50000]+=fact1


np.save('et_4992',energy_transfer)

x=np.linspace(-2500,2500,100001)
plt.plot(x,energy_transfer)
plt.show()


x2=np.linspace(0,50000,5000)
plt.plot(x2,spectrum)
plt.show()




point=0
energy_transfer2 = np.zeros(1001)
for n in xrange(len(events)):
    if n%10000==0:
        print n
    while (events[n,1]>=event_index[point]):
        point+=1
    tof = events[n,0]/10.-52.
    #spectrum[tof/10]+=1
    c=chopper[point-1]-590.
    for ii in range(1,1000):
        ei=ii/20
        i = 23.2868/math.sqrt(ei/sss)*1e6
        #ei=(23.2868/i*1e6)**2*sss
        ef=(2.00098/(tof-i*24.19993/23.2868)*1e6)**2*sss #2.00098 1.85098
        ij=int(((i-c)/s)%255)
        if ij in choppersequence:
            fact1 = 0.5
        else:
            fact1 = -0.5
        de=ef-ei
        print n,count,tof,c,i,ei,ef,ef-ei,ij,fact1
        if abs(de)<2.5:
            energy_transfer2[de*2e4+500]+=fact1


np.save('et2_4992',energy_transfer2)


x=np.linspace(-500,500,1001)
plt.plot(x,energy_transfer2)
plt.show()



point=0
energy_transfer3 = np.zeros(1001)
for n in xrange(len(events)):
    if n%10000==0:
        print n
    while (events[n,1]>=event_index[point]):
        point+=1
    tof = events[n,0]/10.-52.
    #spectrum[tof/10]+=1
    c=chopper[point-1]-590.
    for ii in range(1000,50000,10):
        ei=ii/20
        i = 23.2868/math.sqrt(ei/sss)*1e6
        #ei=(23.2868/i*1e6)**2*sss
        ef=(2.00098/(tof-i*24.19993/23.2868)*1e6)**2*sss #2.00098 1.85098
        ij=int(((i-c)/s)%255)
        if ij in choppersequence:
            fact1 = 0.5
        else:
            fact1 = -0.5
        de=ef-ei
        print n,count,tof,c,i,ei,ef,ef-ei,ij,fact1
        if abs(de)<2.5:
            energy_transfer3[de*2e4+500]+=fact1


np.save('et2_4992',energy_transfer3)


x=np.linspace(-500,500,1001)
plt.plot(x,energy_transfer3)
plt.show()

