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

f=open(choppersequence_file)
choppersequence = f.readlines() # listed is open/non-absorbing
choppersequence = map(int,choppersequence)
f.close()

#events = LoadEventPreNexus(das_file+"_neutron_event.dat",das_file+"_pulseid.dat")

events = np.fromfile(das_file+"_neutron_event.dat",dtype=(np.uint32,2))
###len(events) = 10146570881
###eventPixelID == 4992: 97004

count=0
for n in xrange(len(events)):
    if events[n,1]==4992:
        count+=1

print count


np.save('event_374_4992',out)

