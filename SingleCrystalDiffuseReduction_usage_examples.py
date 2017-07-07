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


# Corelli, Single file
SingleCrystalDiffuseReduction(Filename='CORELLI_29782',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1')

Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_corelli_single.png', vmin=0,vmax=1e-5)
SaveMD(InputWorkspace='output', Filename='corelli_single.nxs')

# Corelli, multiple files
SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817:5',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1')

Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_corelli_multiple.png', vmin=0,vmax=1e-5)
SaveMD(InputWorkspace='output', Filename='corelli_multiple.nxs')

# Corelli, Single file with symmetry
SingleCrystalDiffuseReduction(Filename='CORELLI_29782',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_corelli_single_sym.png', vmin=0,vmax=1e-5)
SaveMD(InputWorkspace='output', Filename='corelli_single_sym.nxs')

# Corelli, multiple files with symmetry
SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817:5',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")


Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_corelli_multiple_sym.png', vmin=0,vmax=1e-5)
SaveMD(InputWorkspace='output', Filename='corelli_multiple_sym.nxs')

# Corelli, multiple files with symmetry and background substraction
SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817:5',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")


Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_corelli_multiple_sym_bkg.png', vmin=0,vmax=1e-5)
SaveMD(InputWorkspace='output', Filename='corelli_multiple_sym_bkg.nxs')

# Reading in elastic Corelli autoreduced data
SingleCrystalDiffuseReduction(Filename=','.join('/SNS/CORELLI/IPTS-15526/shared/autoreduce/CORELLI_'+str(run)+'_elastic.nxs' for run in range(29782,29818,5)),
                              Background='/SNS/CORELLI/IPTS-15796/shared/autoreduce/CORELLI_28124_elastic.nxs',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_corelli_multiple_sym_bkg_elastic.png', vmin=0,vmax=1e-5)
SaveMD(InputWorkspace='output', Filename='corelli_multiple_sym_bkg_elastic.nxs')

# Defining the axis to be [H,H,0], [H,-H,0], [0,0,L]
SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817:5',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-17.5875,17.5875,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_corelli_multiple_sym_bkg_HH0.png', vmin=0,vmax=1e-5,aspect=1)
SaveMD(InputWorkspace='output', Filename='corelli_multiple_sym_bkg_HH0.nxs')

# TOPAZ example using TOF filter and DetCal
SingleCrystalDiffuseReduction(Filename='TOPAZ_23567:23582:3',
                              Background='TOPAZ_23195',
                              FilterByTofMin=500,
                              FilterByTofMax=16600,
                              SolidAngle='/SNS/TOPAZ/IPTS-15526/shared/calibration/solidAngle23189.nxs',
                              Flux='/SNS/TOPAZ/IPTS-15526/shared/calibration/spectra23189.nxs',
                              UBMatrix='/SNS/TOPAZ/IPTS-15526/shared/2017A-data/100K_fe_0p10/100K_Hexagonal_P.mat',
                              OutputWorkspace='output',
                              DetCal='/SNS/TOPAZ/IPTS-15526/shared/calibration/TOPAZ_2017A.DetCal',
                              BinningDim0='-10.05,10.05,201',
                              BinningDim1='-10.05,10.05,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

Plot2DMD(mtd['output'], 'SingleCrystalDiffuseReduction_topaz.png', vmin=0,vmax=5e-5)
SaveMD(InputWorkspace='output', Filename='topaz_multiple_sym_bkg.nxs')
