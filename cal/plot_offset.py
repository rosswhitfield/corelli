from mantid.simpleapi import *
import numpy as np
import math
import matplotlib.pyplot as plt

offset=LoadNexus(Filename='/SNS/users/rwp/COR_525_offset.nxs', OutputWorkspace='offset')
off=offset.extractY().flatten()
fixed=LoadNexus(Filename='/SNS/users/rwp/COR_525_offset_fixed.nxs', OutputWorkspace='fixed')
fix=fixed.extractY().flatten()

plt.plot(off)
plt.plot(fix)
plt.show()


