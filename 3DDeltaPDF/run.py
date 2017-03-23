from mantid.simpleapi import LoadMD, CreateMDHistoWorkspace
from mantid.geometry import SpaceGroupFactory
from astropy.convolution import convolve, convolve_fft, Gaussian1DKernel
import numpy as np
import matplotlib.pyplot as plt

filename='/SNS/CORELLI/IPTS-16344/shared/symm_007K_long_all_ub_13feb.nxs'
filename='/home/rwp/symm_007K_long_all_ub_13feb_small.nxs'
space_group='F 2 3'

ws=LoadMD(filename,LoadHistory=False)

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

signal=ws.getSignalArray().copy()

# Do something with nan's and inf's
signal[np.isnan(signal)]=0
signal[np.isinf(signal)]=0

fft=np.fft.fftshift(np.fft.fftn(np.fft.fftshift(signal)))
out=(fft*np.conj(fft)).real

# convolve
signal=ws.getSignalArray().copy()

G1D = Gaussian1DKernel(2).array
G3D = G1D * G1D.reshape((-1,1)) * G1D.reshape((-1,1,1))
convolved = convolve(signal, G3D)

convolved_fft=np.fft.fftshift(np.fft.fftn(np.fft.fftshift(convolved)))
convolved_out=(convolved_fft*np.conj(convolved_fft)).real

# Create output workspace
CreateMDHistoWorkspace(SignalInput=out,
                       ErrorInput=out**2,
                       Dimensionality=3,
                       Extents=np.array(dim_list).flatten(),
                       NumberOfBins=signal.shape,
                       Names='x,y,z',
                       Units='A,A,A',
                       OutputWorkspace='output')
