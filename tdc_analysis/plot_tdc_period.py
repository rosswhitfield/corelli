#!/usr/bin/env python

from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt


ws = LoadEventNexus('CORELLI_103083',MetaDataOnly=True)
tdc = ws.getRun().getProperty("chopper4_TDC").times
wl =  ws.getRun().getProperty("BL9:Chop:Skf4:WavelengthSet").value[0]
phaseDelay =  ws.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").value[0]

diff = (tdc[1:] - tdc[:-1]).astype(np.int64)/100



#plt.plot(np.bincount(diff))
#plt.show()
