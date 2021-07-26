from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots

filename='CORELLI_29782'
#filename='CORELLI_29782:29817'

Load(Filename=filename, OutputWorkspace='data')

SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
Load(Filename=SolidAngle, OutputWorkspace='SolidAngle')
Load(Filename=Flux, OutputWorkspace= 'Flux')
MaskDetectors(Workspace='data', MaskedWorkspace='SolidAngle')
ConvertUnits(InputWorkspace='data',OutputWorkspace='data',Target='Momentum')
CropWorkspaceForMDNorm(InputWorkspace='data',
                       XMin=2.5,
                       XMax=10,
                       OutputWorkspace='data')
LoadIsawUB(InputWorkspace='data',Filename=UBMatrix)
SetGoniometer(Workspace='data',Axis0='BL9:Mot:Sample:Axis1,0,1,0,1')
min_vals,max_vals=ConvertToMDMinMaxGlobal(InputWorkspace='data',
                                          QDimensions='Q3D',
                                          dEAnalysisMode='Elastic',
                                          Q3DFrames='Q')
ConvertToMD(InputWorkspace='data',
            QDimensions='Q3D',
            dEAnalysisMode='Elastic',
            Q3DFrames='Q_sample',
            OutputWorkspace='md',
            MinValues=min_vals,
            MaxValues=max_vals)
RecalculateTrajectoriesExtents(InputWorkspace= 'md', OutputWorkspace='md')

MDNorm(InputWorkspace='md',
       SolidAngleWorkspace='SolidAngle',
       FluxWorkspace='Flux',
       QDimension0='1,1,0',
       QDimension1='1,-1,0',
       QDimension2='0,0,1',
       Dimension0Name='QDimension0',
       Dimension0Binning='-10.0,0.025,10.0',
       Dimension1Name='QDimension1',
       Dimension1Binning='-10.0,0.025,10.0',
       Dimension2Name='QDimension2',
       Dimension2Binning='-0.1,0.1',
       SymmetryOperations='P 31 2 1',
       OutputWorkspace='result',
       OutputDataWorkspace='dataMD',
       OutputNormalizationWorkspace='normMD')

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['result'], vmin=0, vmax=2e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_300K_{filename}.png', dpi=300)

MDNorm(InputWorkspace='md',
       SolidAngleWorkspace='SolidAngle',
       FluxWorkspace='Flux',
       QDimension0='1,1,0',
       QDimension1='1,-1,0',
       QDimension2='0,0,1',
       Dimension0Name='QDimension0',
       Dimension0Binning='-10.0,0.025,10.0',
       Dimension1Name='QDimension1',
       Dimension1Binning='-10.0,0.025,10.0',
       Dimension2Name='QDimension2',
       Dimension2Binning='-0.1,0.1',
       OutputWorkspace='result',
       OutputDataWorkspace='dataMD',
       OutputNormalizationWorkspace='normMD')

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['result'], vmin=0, vmax=2e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_300K_{filename}_no_sym.png', dpi=300)
