from mantid.simpleapi import LoadMD, CreateMDHistoWorkspace
from mantid.geometry import SpaceGroupFactory
from astropy.convolution import convolve, convolve_fft, Gaussian1DKernel, Gaussian2DKernel
import numpy as np
import matplotlib.pyplot as plt
import time

filename='/SNS/CORELLI/IPTS-16344/shared/symm_007K_long_all_ub_13feb.nxs'
space_group='F 2 3'

ws=LoadMD(filename)

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

start=time.time()
convolved = convolve(signal, G3D)
end=time.time()
print(end-start)
start=time.time()
convolved_fft = convolve_fft(signal, G3D, allow_huge=True)
end=time.time()
print(end-start)


s=signal[251]

start=time.time()
convolved = convolve(s, Gaussian2DKernel(2))
end=time.time()
print(end-start)
start=time.time()
convolved_fft = convolve_fft(s, Gaussian2DKernel(2))
end=time.time()
print(end-start)
G2D = G1D * G1D.reshape((-1,1))
start=time.time()
convolved = convolve(s, G2D)
end=time.time()
print(end-start)
start=time.time()
convolved_fft = convolve_fft(s, G2D)
end=time.time()
print(end-start)
