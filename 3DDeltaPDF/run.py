from mantid.simpleapi import LoadMD, CreateMDHistoWorkspace
from mantid.geometry import SpaceGroupFactory
from astropy.convolution import convolve
import numpy as np

filename='/SNS/CORELLI/IPTS-16344/shared/symm_007K_long_all_ub_13feb.nxs'
space_group='F 2 3'



ws=LoadMD(filename)
# Check alignment
if not np.all(ws.getExperimentInfo(0).run().getLogData('W_MATRIX').value ==
              [ 1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  1.]):
    print('Not alligned with HKL')
    exit()
# Check centered on zero
for d in range(ws.getNumDims()):
    dim = ws.getDimension(d)
    
