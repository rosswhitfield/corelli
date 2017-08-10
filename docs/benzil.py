# Vanadium for normalisation
Load(Filename='CORELLI_28119-28123', OutputWorkspace='van')
ConvertUnits(InputWorkspace='van', OutputWorkspace='van', Target='Momentum')
CropWorkspace(InputWorkspace='van', OutputWorkspace='van', XMin='2.5', XMax='10')
# Get Solid Angle
Rebin(InputWorkspace='van', OutputWorkspace='sa', Params='2.5,10,10', PreserveEvents='0')
SaveNexus(InputWorkspace='sa', Filename='SolidAngle.nxs')
# Get Flux
SumSpectra(InputWorkspace='van', OutputWorkspace='flux')
CompressEvents(InputWorkspace='flux', OutputWorkspace='flux')
Rebin(InputWorkspace='flux', OutputWorkspace='flux', Params='2.5,10,10')
flux=mtd['flux']
for i in range(flux.getNumberHistograms()):
    el=flux.getSpectrum(i)
    el.divide(flux.readY(i)[0],0)
Rebin(InputWorkspace='flux', OutputWorkspace='flux', Params='2.5,10,10')
IntegrateFlux(InputWorkspace='flux', OutputWorkspace='flux')
SaveNexus(InputWorkspace='flux', Filename='Spectrum.nxs')

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_29782:29817:10',
                                     FilterByTofMin=1000,
                                     FilterByTofMax=16666,
                                     SetGoniometer=True,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                                     OutputWorkspace='md')

FindPeaksMD(InputWorkspace='md',DensityThresholdFactor=50000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks',CellType='Hexagonal',Apply=True)
SaveIsawUB(InputWorkspace='peaks', Filename='benzil.mat')

SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817:10',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='SolidAngle.nxs',
                              Flux='Spectrum.nxs',
                              UBMatrix="benzil.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-7.5375,7.5375,201',
                              BinningDim1='-13.165625,13.165625,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")
