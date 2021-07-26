from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots

filename = 'CORELLI_29715'
SingleCrystalDiffuseReduction(Filename=filename,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output1',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              QDimension0='1,1,0',
                              QDimension1='1,-1,0',
                              QDimension2='0,0,1',
                              Dimension0Binning='-7.5375,0.025,7.5375',
                              Dimension1Binning='-13.165625,0.04366708333,13.165625',
                              Dimension2Binning='-0.1,0.1',
                              SymmetryOperations="P 31 2 1")

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['output1'], vmin=2e-6, vmax=1e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_100K_{filename}.png', dpi=300)

filename = 'CORELLI_29715:29750'
SingleCrystalDiffuseReduction(Filename=filename,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              QDimension0='1,1,0',
                              QDimension1='1,-1,0',
                              QDimension2='0,0,1',
                              Dimension0Binning='-7.5375,0.025,7.5375',
                              Dimension1Binning='-13.165625,0.04366708333,13.165625',
                              Dimension2Binning='-0.1,0.1',
                              SymmetryOperations="P 31 2 1")

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['output'], vmin=2e-6, vmax=1e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_100K_{filename}.png', dpi=300)
