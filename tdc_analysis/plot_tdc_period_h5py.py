#!/usr/bin/env python

import h5py
import numpy as np
import matplotlib.pyplot as plt


#ws = LoadEventNexus('CORELLI_103083',MetaDataOnly=True)
f = h5py.File('/SNS/CORELLI/IPTS-23139/nexus/CORELLI_103083.nxs.h5', 'r')
#tdc = ws.getRun().getProperty("chopper4_TDC").times
tdc = f['entry/DASlogs/chopper4_TDC/value'].value.astype(np.int64)
#wl =  ws.getRun().getProperty("BL9:Chop:Skf4:WavelengthSet").value[0]
wl = f['entry/DASlogs/BL9:Chop:Skf4:WavelengthSet/value'].value[0]
#phaseDelay =  ws.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").value[0]
phaseDelay = f['entry/DASlogs/BL9:Chop:Skf4:PhaseTimeDelaySet/value'].value[0]

diff = (tdc[1:] - tdc[:-1])/100

unique, unique_counts = np.unique(diff, return_counts=True)



plt.plot(unique, unique_counts)
plt.xlabel("Chopper period (100ns)")
plt.ylabel("Period frequency")
plt.show()
