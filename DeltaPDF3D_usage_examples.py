import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mantid.simpleapi import *
import numpy as np

def dim2array(d):
    dmin=d.getMinimum()
    dmax=d.getMaximum()
    dstep=d.getBinWidth()
    return np.arange(dmin+dstep/2,dmax,dstep)

def Plot2DMD(ws,filename,**kwargs):
    dims=ws.getNonIntegratedDimensions()
    if len(dims)!=2:
        raise ValueError("The workspace dimensionality is not 2")
    dimx=dims[0]
    x=dim2array(dimx)
    dimy=dims[1]
    y=dim2array(dimy)
    intensity=ws.getSignalArray().copy()
    intensity=intensity.squeeze()
    intensity=np.ma.masked_where(np.isnan(intensity),intensity)
    XX,YY=np.meshgrid(x,y,indexing='ij')
    plt.clf()
    fig = plt.pcolormesh(XX,YY,intensity,**kwargs)
    plt.xlabel(dimx.name+' ('+dimx.getUnits()+')')
    plt.ylabel(dimy.name+' ('+dimy.getUnits()+')')
    plt.axes().set_aspect(1)
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(filename)

# Usage axamples
DeltaPDF3D_MDE = CreateMDWorkspace(Dimensions='3', Extents='-3.1,3.1,-3.1,3.1,-0.1,0.1', Names='[H,0,0],[0,K,0],[0,0,L]',
                                   Units='rlu,rlu,rlu', SplitInto='4',Frames='HKL,HKL,HKL')
# Add some Bragg peaks
for h in range(-3,4):
    for k in range(-3,4):
        FakeMDEventData(DeltaPDF3D_MDE, PeakParams='100,'+str(h)+','+str(k)+',0,0.1', RandomSeed='1337')
# Add addiontal peaks on [0.5,0.5,0.5] type positions
# This would correspond to negative substitutional correlations
for h in [-2.5,-1.5,-0.5,0.5,1.5,2.5]:
    for k in range(-3,4):
        FakeMDEventData(DeltaPDF3D_MDE, PeakParams='20,'+str(h)+','+str(k)+',0,0.1', RandomSeed='13337')
# Create MHHistoWorkspace
BinMD(InputWorkspace='DeltaPDF3D_MDE', AlignedDim0='[H,0,0],-3.05,3.05,61', AlignedDim1='[0,K,0],-3.05,3.05,61',
      AlignedDim2='[0,0,L],-0.1,0.1,1', OutputWorkspace='DeltaPDF3D_MDH')


Plot2DMD(mtd['DeltaPDF3D_MDH'], 'DeltaPDF3D_testWS.png', vmin=0,vmax=20)


DeltaPDF3D(InputWorkspace='DeltaPDF3D_MDH',OutputWorkspace='fft',
           RemoveReflections=False,Convolution=False)

Plot2DMD(mtd['fft'], 'DeltaPDF3D_fft1.png', vmin=-1000,vmax=1000)

DeltaPDF3D(InputWorkspace='DeltaPDF3D_MDH',OutputWorkspace='fft2',IntermediateWorkspace='int2',
           RemoveReflections=True,Size=0.3,Convolution=False)

Plot2DMD(mtd['int2'], 'DeltaPDF3D_int2.png', vmin=0,vmax=20)
Plot2DMD(mtd['fft2'], 'DeltaPDF3D_fft2.png', vmin=-200,vmax=200)

DeltaPDF3D(InputWorkspace='DeltaPDF3D_MDH',OutputWorkspace='fft3',IntermediateWorkspace='int3',
           RemoveReflections=True,Size=0.3,CropSphere=True,SphereMax=3,Convolution=False)

Plot2DMD(mtd['int3'], 'DeltaPDF3D_int3.png', vmin=0,vmax=20)
Plot2DMD(mtd['fft3'], 'DeltaPDF3D_fft3.png', vmin=-200,vmax=200)

DeltaPDF3D(InputWorkspace='DeltaPDF3D_MDH',OutputWorkspace='fft3',IntermediateWorkspace='int3',
           RemoveReflections=True,Size=0.3,CropSphere=True,SphereMax=3,Convolution=False,FillValue=0.1)

Plot2DMD(mtd['int3'], 'DeltaPDF3D_int3_2.png', vmin=0,vmax=20)
Plot2DMD(mtd['fft3'], 'DeltaPDF3D_fft3_2.png', vmin=-200,vmax=200)

DeltaPDF3D(InputWorkspace='DeltaPDF3D_MDH',OutputWorkspace='fft4',IntermediateWorkspace='int4',
           RemoveReflections=True,Size=0.3,CropSphere=True,SphereMax=3,Convolution=True)

Plot2DMD(mtd['int4'], 'DeltaPDF3D_int4.png', vmin=0,vmax=0.2)
Plot2DMD(mtd['fft4'], 'DeltaPDF3D_fft4.png', vmin=-50,vmax=50)



DeltaPDF3D(InputWorkspace='DeltaPDF3D_MDH',OutputWorkspace='fft5',IntermediateWorkspace='int5',
           RemoveReflections=True,Size=0.3,CropSphere=True,SphereMax=3,Convolution=True,Deconvolution=True)

Plot2DMD(mtd['int5'], 'DeltaPDF3D_int5.png', vmin=0,vmax=0.2)
Plot2DMD(mtd['fft5'], 'DeltaPDF3D_fft5.png', vmin=-50,vmax=50)
DivideMD('fft4','fft5',OutputWorkspace='deconv')
Plot2DMD(mtd['deconv'], 'DeltaPDF3D_deconv.png', vmin=0,vmax=1)
