from mantid.simpleapi import *
import matplotlib.pyplot as plt
from mantid import plots

filename = 'CORELLI_29782'
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
                              Dimension2Binning='-0.5,0.5')

SaveMD(mtd['output1'], f'Benzil_300K_{filename}.nxs')

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['output1'], vmin=2e-6, vmax=1e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_300K_{filename}.png', dpi=300)

filename = 'CORELLI_29782:29817'
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
                              Dimension2Binning='-0.5,0.5')

SaveMD(mtd['output'], f'Benzil_300K_{filename}.nxs')

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['output'], vmin=2e-6, vmax=1e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_300K_{filename}.png', dpi=300)

filename = 'CORELLI_29782'
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
                              Dimension2Binning='-0.5,0.5',
                              SymmetryOperations="P 31 2 1")

SaveMD(mtd['output1'], f'Benzil_300K_{filename}_sym.nxs')

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['output1'], vmin=2e-6, vmax=1e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_300K_{filename}_sym.png', dpi=300)

filename = 'CORELLI_29782:29817'
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
                              Dimension2Binning='-0.5,0.5',
                              SymmetryOperations="P 31 2 1")

SaveMD(mtd['output'], f'Benzil_300K_{filename}_sym.nxs')

fig, ax = plt.subplots(subplot_kw={'projection':'mantid'})
c = ax.pcolormesh(mtd['output'], vmin=2e-6, vmax=1e-5)
fig.colorbar(c)
fig.savefig(f'Benzil_300K_{filename}_sym.png', dpi=300)

from mantid import plots
import matplotlib.pyplot as plt
from mantid.simpleapi import *

filename = 'CORELLI_29782'
output1=LoadMD(f'Benzil_300K_{filename}.nxs')
output2=LoadMD(f'Benzil_300K_{filename}_sym.nxs')

filename = 'CORELLI_29782:29817'
output3=LoadMD(f'Benzil_300K_{filename}.nxs')
output4=LoadMD(f'Benzil_300K_{filename}_sym.nxs')

fig = plt.figure(figsize = (6,6))
ax1 = fig.add_subplot(221, projection = 'mantid')
ax2 = fig.add_subplot(222, projection = 'mantid', sharey=ax1)
ax3 = fig.add_subplot(223, projection = 'mantid', sharex=ax1)
ax4 = fig.add_subplot(224, projection = 'mantid', sharex=ax1, sharey=ax1)

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax2.get_yticklabels(), visible=False)
plt.setp(ax4.get_yticklabels(), visible=False)

vmin=2e-6
vmax=8e-6

ax1.pcolormesh(mtd['output1'], vmin=vmin, vmax=vmax)
ax2.pcolormesh(mtd['output2'], vmin=vmin, vmax=vmax)
ax3.pcolormesh(mtd['output3'], vmin=vmin, vmax=vmax)
ax4.pcolormesh(mtd['output4'], vmin=vmin, vmax=vmax)

ax1.set_xlabel('')
ax1.set_ylabel('[H,-H,0]')
ax2.set_xlabel('')
ax2.set_ylabel('')
ax3.set_ylabel('[H,-H,0]')
ax3.set_xlabel('[H,H,0]')
ax4.set_ylabel('')
ax4.set_xlabel('[H,H,0]')

ax1.text(0.05, 0.9, '(a)', transform=ax1.transAxes, size=15)
ax2.text(0.85, 0.9, '(b)', transform=ax2.transAxes, size=15)
ax3.text(0.05, 0.9, '(c)', transform=ax3.transAxes, size=15)
ax4.text(0.85, 0.9, '(d)', transform=ax4.transAxes, size=15, color='white')

plt.subplots_adjust(wspace=0, hspace=0)

fig.savefig('Benzil_300K.png', dpi=300)
fig.savefig('Benzil_300K.eps')

