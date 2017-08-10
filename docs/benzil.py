


FindPeaksMD(InputWorkspace='md',DensityThresholdFactor=50000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=15)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellOfType(PeaksWorkspace='peaks',CellType='Hexagonal',Apply=True)
SaveIsawUB(InputWorkspace='peaks', Filename='benzil.mat')




SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817:10',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs',
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
