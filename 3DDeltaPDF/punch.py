from mantid.simpleapi import LoadMD, CreateMDHistoWorkspace
from mantid.geometry import SpaceGroupFactory
from astropy.convolution import convolve, convolve_fft, Gaussian1DKernel
import numpy as np
import matplotlib.pyplot as plt

filename='/SNS/CORELLI/IPTS-16344/shared/symm_007K_long_all_ub_13feb.nxs'
space_group='F 2 3'

ws=LoadMD(filename)

# Check alignment
if not np.all(ws.getExperimentInfo(0).run().getLogData('W_MATRIX').value ==
              [ 1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  1.]):
    print('Not alligned with HKL')
    exit()

# Check dimensions
# Check centered on zero
# Should also check center bin is 0
dim_list=[]
dim_names=['[H,0,0]','[0,K,0]','[0,0,L]']
for d in range(ws.getNumDims()):
    dim = ws.getDimension(d)
    if dim.name not in dim_names:
        print("Dimensions must be one of ",dim_names)
        exit()
    if dim.getMaximum() != -dim.getMinimum():
        print('Workspace dimensions must be centered on zero')
        exit()
    #dim_list.append((dim.getNBins(), (dim.getMaximum()-dim.getMinimum())/dim.getNBins()))
    fft_dim=np.fft.fftshift(np.fft.fftfreq(dim.getNBins(), (dim.getMaximum()-dim.getMinimum())/dim.getNBins()))
    dim_list.append((fft_dim[0],fft_dim[-1]))

dimX=ws.getXDimension()
dimY=ws.getYDimension()
dimZ=ws.getZDimension()



signal=ws.getSignalArray().copy()

sg=SpaceGroupFactory.createSpaceGroup(space_group)

X=np.linspace(dimX.getMinimum(),dimX.getMaximum(),dimX.getNBins()+1)
Y=np.linspace(dimY.getMinimum(),dimY.getMaximum(),dimY.getNBins()+1)
Z=np.linspace(dimZ.getMinimum(),dimZ.getMaximum(),dimZ.getNBins()+1)


for h in range(int(np.ceil(dimX.getMinimum())), int(np.floor(dimX.getMaximum()))+1):
    for k in range(int(np.ceil(dimY.getMinimum())), int(np.floor(dimY.getMaximum()))+1):
        for l in range(int(np.ceil(dimZ.getMinimum())), int(np.floor(dimZ.getMaximum()))+1):
            hkl=[h,k,l]
            print(hkl,sg.isAllowedReflection(hkl))
