import numpy as np
import os
from struct import *

das_file="/SNS/users/srosenkranz/corelli/DAS_374/DAS_374"

count = 0
f = open(das_file+"_neutron_event.dat")
f.seek(0,os.SEEK_END)
size = f.tell()/8
f.seek(0,os.SEEK_SET)
print 'Events =',size

events = np.zeros((1e8,2),dtype=np.int64)

count = 0
for n in xrange(size):
    a=f.read(8)
    (tof,pid) = unpack('ii',a)
    if pid > 4960 and pid < 5024:
        events[count] = (tof,n)
        count += 1
        if (count%10000==0):
            print count,n

print count

f.close()

out = events[:count]

np.save('events_374_4960-5024',out)
