ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_82204:82232', SetGoniometer=True, Axis0='BL9:Mot:Sample:Axis3,0,1,0,1', OutputWorkspace='md')
FindPeaksMD(InputWorkspace='md', PeakDistanceThreshold=0.25, DensityThresholdFactor=10000000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=1, MaxD=10)
SaveIsawUB('peaks', '/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat')

SingleCrystalDiffuseReduction(Filename='CORELLI_82204:82232',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/SolidAngle_CCR_20181019tot.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/Spectrum_CCR_20181019tot.nxs',
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis3,0,1,0,1",
                              UBMatrix="/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat",
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')


SingleCrystalDiffuseReduction(Filename='CORELLI_82204:82232',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/SolidAngle_CCR_20181019tot.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/Spectrum_CCR_20181019tot.nxs',
                              OutputWorkspace='sym',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis3,0,1,0,1",
                              UBMatrix="/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat",
                              SymmetryOps='195',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')


SingleCrystalDiffuseReduction(Filename='CORELLI_82204:82232',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/SolidAngle_CCR_20181019tot.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/Spectrum_CCR_20181019tot.nxs',
                              OutputWorkspace='sym_all',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis3,0,1,0,1",
                              UBMatrix="/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat",
                              SymmetryOps='225',
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501')
SaveMD('sym_all', '/SNS/users/rwp/corelli/IPTS-20534/PMN/sym_all.nxs')

LoadMD(Filename='/SNS/users/rwp/corelli/IPTS-20534/PMN/sym_all.nxs', LoadHistory=False, OutputWorkspace='PMN_5k')
SliceMDHisto(InputWorkspace='PMN_5k', Start='80,80,80', End='421,421,421', OutputWorkspace='slice')
DeltaPDF3D(InputWorkspace='slice', IntermediateWorkspace='ints', OutputWorkspace='outs', Method='KAREN', SphereMin='8.98847e+307', SphereMax='8.98847e+307', Convolution=False)
SaveMD('outs', '/SNS/users/rwp/corelli/IPTS-20534/PMN/sym_all_slice_pdf.nxs')

SaveMDWorkspaceToVTK('outs', '/SNS/users/rwp/corelli/IPTS-20534/PMN/sym_all_slice_pdf.vts')

# With background

SingleCrystalDiffuseReduction(Filename='CORELLI_82204:82232',
                              Background='CORELLI_82129',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/SolidAngle_CCR_20181019tot.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/Spectrum_CCR_20181019tot.nxs',
                              OutputWorkspace='output_subBkg',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis3,0,1,0,1",
                              UBMatrix="/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat",
                              BinningDim0='-10.02,10.02,501',
                              BinningDim1='-10.02,10.02,501',
                              BinningDim2='-10.02,10.02,501',
                              KeepTemporaryWorkspaces=True)

SingleCrystalDiffuseReduction(Filename='CORELLI_82204:82232',
                              Background='CORELLI_82129',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/SolidAngle_CCR_20181019tot.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/Spectrum_CCR_20181019tot.nxs',
                              OutputWorkspace='output_subBkg_750',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis3,0,1,0,1",
                              UBMatrix="/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat",
                              BinningDim0='-7.51,7.51,751',
                              BinningDim1='-7.51,7.51,751',
                              BinningDim2='-7.51,7.51,751',
                              KeepTemporaryWorkspaces=True)


SingleCrystalDiffuseReduction(Filename='CORELLI_82204:82232',
                              Background='CORELLI_82129',
                              SolidAngle='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/SolidAngle_CCR_20181019tot.nxs',
                              Flux='/SNS/CORELLI/shared/Vanadium/2018B_1019_CCR/Spectrum_CCR_20181019tot.nxs',
                              OutputWorkspace='sym_all_subBkg',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis3,0,1,0,1",
                              UBMatrix="/SNS/users/rwp/corelli/IPTS-20534/PMN/PMN_5K.mat",
                              SymmetryOps='225',
                              BinningDim0='-7.51,7.51,751',
                              BinningDim1='-7.51,7.51,751',
                              BinningDim2='-7.51,7.51,751')
SaveMD('sym_all_subBkg', '/SNS/users/rwp/corelli/IPTS-20534/PMN/sym_all_subBkg.nxs')
