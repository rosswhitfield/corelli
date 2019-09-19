#!/usr/bin/env python

import h5py
import numpy as np
import matplotlib.pyplot as plt
import glob

filenames = glob.glob('/SNS/CORELLI/IPTS-22211/nexus/CORELLI_*.nxs.h5')

for filename in filenames:
    with h5py.File(filename, 'r') as f:
        tdc = f['entry/DASlogs/chopper4_TDC/time'].value
        wl = f['entry/DASlogs/BL9:Chop:Skf4:WavelengthSet/value'].value[0]
        phaseDelay = f['entry/DASlogs/BL9:Chop:Skf4:PhaseTimeDelaySet/value'].value[0]
        diff = (tdc[1:] - tdc[:-1])/100
        plt.clf()
        plt.plot(diff[:100], tdc[:100])
        plt.xlabel("Chopper period (100ns)")
        plt.ylabel("Time (ns)")
        plt.title("{} - wavelength = {} - Phase Delay = {:.2f}".format(filename.split('/')[-1],wl, phaseDelay))
        plt.xlim(34060, 34100)
        plt.savefig("images/"+filename.split('/')[-1]+"_p_v_t.png")
