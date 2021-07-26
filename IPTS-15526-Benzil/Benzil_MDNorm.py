from mantid.simpleapi import *

runs=range(29782,29818)


Load(Filename='CORELLI_29782', OutputWorkspace='data')
Load(Filename='/SNS/users/rwp/mantid/build/ExternalData/Testing/Data/SystemTest/SingleCrystalDiffuseReduction_SA.nxs', OutputWorkspace='SolidAngle')
Load(Filename='/SNS/users/rwp/mantid/build/ExternalData/Testing/Data/SystemTest/SingleCrystalDiffuseReduction_Flux.nxs', OutputWorkspace= 'Flux')
MaskDetectors(Workspace='data', MaskedWorkspace='SolidAngle')
ConvertUnits(InputWorkspace='data',OutputWorkspace='data',Target='Momentum')
CropWorkspaceForMDNorm(InputWorkspace='data',
                       XMin=2.5,
                       XMax=10,
                       OutputWorkspace='data')
LoadIsawUB(InputWorkspace='data',Filename='/SNS/users/rwp/mantid/build/ExternalData/Testing/Data/SystemTest/SingleCrystalDiffuseReduction_UB.mat')
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
       Dimension0Binning='-10.0,0.1,10.0',
       Dimension1Name='QDimension1',
       Dimension1Binning='-10.0,0.1,10.0',
       Dimension2Name='QDimension2',
       Dimension2Binning='-0.1,0.1',
       SymmetryOperations='P 31 2 1',
       OutputWorkspace='result',
       OutputDataWorkspace='dataMD',
       OutputNormalizationWorkspace='normMD')

import matplotlib.pyplot as plt
from mantid import plots

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['result'])
fig.colorbar(c)
fig.savefig('Benzil_300K.png')
