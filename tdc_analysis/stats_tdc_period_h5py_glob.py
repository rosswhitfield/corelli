#!/usr/bin/env python

import h5py
import numpy as np
import glob

filenames = glob.glob('/SNS/CORELLI/IPTS-22211*/nexus/CORELLI_*.nxs.h5')
filenames.sort()
fout = open("stats.txt", "w")
for filename in filenames:
    with h5py.File(filename, 'r') as f:
        try:
            tdc = f['entry/DASlogs/chopper4_TDC/value'].value.astype(np.int64)
            wl = f['entry/DASlogs/BL9:Chop:Skf4:WavelengthSet/value'].value[0]
            phaseDelay = f['entry/DASlogs/BL9:Chop:Skf4:PhaseTimeDelaySet/value'].value[0]
            diff = (tdc[1:] - tdc[:-1])/100
            diff2 = diff[np.logical_and(diff<34100, diff>34060)]
            print("{} - wavelength = {} - Phase Delay = {:.2f} - mean = {:.2f} - std = {:.2f}".format(filename.split('/')[-1],wl, phaseDelay, np.mean(diff2), np.std(diff2)))
            fout.write("{} - wavelength = {} - Phase Delay = {:.2f} - mean = {:.2f} - std = {:.2f}\n".format(filename.split('/')[-1],wl, phaseDelay, np.mean(diff2), np.std(diff2)))
        except KeyError:
            pass
fout.close()
