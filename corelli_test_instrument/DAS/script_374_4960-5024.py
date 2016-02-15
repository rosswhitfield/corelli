import numpy as np
from pylab import *
from struct import *
import os
import math
#from mantid.simpleapi import *

das_file="/SNS/users/srosenkranz/corelli/DAS_374/DAS_374"
chopper_file ="/SNS/users/srosenkranz/corelli/timingdata/chopper_374_3.dat"
pulse_file   ="/SNS/users/srosenkranz/corelli/timingdata/rtdl_374_3.dat"
choppersequence_file = "/SNS/users/srosenkranz/corelli/choppersequence255.txt"

#f=open(choppersequence_file)
#choppersequence = f.readlines() # listed is open/non-absorbing
#choppersequence = map(int,choppersequence)
#f.close()

#events = LoadEventPreNexus(das_file+"_neutron_event.dat",das_file+"_pulseid.dat")

#events = np.fromfile(das_file+"_neutron_event.dat",dtype=(np.uint32,2))
###len(events) = 10146570881
###eventPixelID == 4992: 1327277

#dt = np.dtype([('nanoseconds',np.uint32),('seconds',np.uint32),('event_index',np.uint64),('pCurrent',np.float64)])
#pulses = np.fromfile(das_file+"_pulseid.dat",dtype=dt) 

#chopper = np.fromfile(chopper_file,dtype=np.float)
#rtdl_pulses = np.fromfile(pulse_file,dtype=(np.uint32,6))

count = 0
f = open(das_file+"_neutron_event.dat")
f.seek(0,os.SEEK_END)
size = f.tell()/8
f.seek(0,os.SEEK_SET)
print 'Events =',size

events = np.zeros((1e8,2),dtype=np.int64)
#results = np.zeros((5000,5000))

count = 0
for n in xrange(size):
    a=f.read(8)
    (tof,pid) = unpack('ii',a)
    if pid > 4960 and pid < 5024:
        events[count] = (tof,n)
        count += 1
        if (count%10000==0):
            print count,n
        #print count, pid
        #tof = tof/10.-52.
        #pulse = np.searchsorted(pulses['event_index'],n+1)-1
        #print tof,pulse,chopper[pulse]-590.
        #j = int(chopper[pulse]-590.)%256
        #out[(chopper[pulse]-590.)/10.,tof/10.]+=1

print count

f.close()

np.save('events_374_4960-5024_int64',events)
