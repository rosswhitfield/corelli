#!/usr/bin/env python

import h5py
import numpy as np
import matplotlib.pyplot as plt

filename = '/SNS/CORELLI/IPTS-23139/nexus/CORELLI_103083.nxs.h5'
filename = '/SNS/CORELLI/IPTS-20534/nexus/CORELLI_82222.nxs.h5'

f = h5py.File(filename, 'r')
tdc = f['entry/DASlogs/chopper4_TDC/value'].value.astype(np.int64)
wl = f['entry/DASlogs/BL9:Chop:Skf4:WavelengthSet/value'].value[0]
phaseDelay = f['entry/DASlogs/BL9:Chop:Skf4:PhaseTimeDelaySet/value'].value[0]

diff = (tdc[1:] - tdc[:-1])/100

unique, unique_counts = np.unique(diff, return_counts=True)



plt.plot(unique, unique_counts)
plt.xlabel("Chopper period (100ns)")
plt.ylabel("Period frequency")
plt.title("{} - wavelength = {} - Phase Delay = {}".format(filename.split('/')[-1],wl, spaseDelay))
plt.xlim(34060, 34100)
plt.show()
