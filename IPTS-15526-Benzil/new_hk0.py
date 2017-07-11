import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mantid.simpleapi import SingleCrystalDiffuseReduction, SaveMD, mtd
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
    intensity=ws.getSignalArray().copy()
    intensity=intensity.squeeze()
    intensity=np.ma.masked_where(np.isnan(intensity),intensity)
    xx,yy = np.meshgrid(np.linspace(-1,1,301),np.linspace(-1,1,301))
    intensity=np.ma.masked_where(xx**2 + yy**2 > 1,intensity)
    plt.clf()
    fig = plt.imshow(intensity.T,interpolation='nearest',**kwargs)
    plt.axis('off')
    #plt.tight_layout()
    plt.savefig(filename,bbox_inches='tight',pad_inches = 0)

SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='benzil_300k',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-7.525,7.525,301',
                              BinningDim1='-13.16875,13.16875,301',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['benzil_300k'],'/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_300k.png',vmin=0,vmax=1e-5,cmap='hot')
SaveMD('benzil_300k','/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_300k.nxs')

SingleCrystalDiffuseReduction(Filename=','.join('/SNS/CORELLI/IPTS-15526/shared/autoreduce/CORELLI_'+str(run)+'_elastic.nxs' for run in range(29782,29818)),
                              Background='/SNS/CORELLI/IPTS-15796/shared/autoreduce/CORELLI_28124_elastic.nxs',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='benzil_300k_elastic',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-7.525,7.525,301',
                              BinningDim1='-13.16875,13.16875,301',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['benzil_300k_elastic'],'/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_300k_elastic.png',vmin=0,vmax=1e-5,cmap='hot')
SaveMD('benzil_300k_elastic','/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_300k_elastic.nxs')

runs = range(29715,29755)+range(29589,29625)+range(29533,29536)+range(29556,29589)
#runs = range(29556,29589,5)

SingleCrystalDiffuseReduction(Filename=','.join('CORELLI_'+str(r) for r in runs),
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='benzil_100k',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-7.525,7.525,301',
                              BinningDim1='-13.16875,13.16875,301',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['benzil_100k'],'/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_100k.png',vmin=0,vmax=1e-5,cmap='hot')
SaveMD('benzil_100k','/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_100k.nxs')

SingleCrystalDiffuseReduction(Filename=','.join('/SNS/CORELLI/IPTS-15526/shared/autoreduce/CORELLI_'+str(r)+'_elastic.nxs' for r in runs),
                              Background='/SNS/CORELLI/IPTS-15796/shared/autoreduce/CORELLI_28124_elastic.nxs',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='benzil_100k_elastic',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-7.525,7.525,301',
                              BinningDim1='-13.16875,13.16875,301',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['benzil_100k_elastic'],'/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_100k_elastic.png',vmin=0,vmax=1e-5,cmap='hot')
SaveMD('benzil_100k_elastic','/SNS/users/rwp/corelli/IPTS-15526-Benzil/benzil_100k_elastic.nxs')
