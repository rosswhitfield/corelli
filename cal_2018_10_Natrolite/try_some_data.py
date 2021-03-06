from mantid import config
config['loading.multifilelimit']='1000'


Load('CORELLI_81285', OutputWorkspace='CORELLI_81285')
SetGoniometer(Workspace='CORELLI_81285', Axis0='BL9:Mot:Sample:Axis3,0,1,0,1')
ConvertToMD(InputWorkspace='CORELLI_81285', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md_81285')

FindPeaksMD(InputWorkspace='md_81285', PeakDistanceThreshold=0.5, MaxPeaks=2000, OutputWorkspace='peaks_81285')
FindUBUsingFFT(PeaksWorkspace='peaks_81285', MinD=5, MaxD=20)
ShowPossibleCells(PeaksWorkspace='peaks_81285')
SelectCellWithForm(PeaksWorkspace='peaks_81285', FormNumber=26, Apply=True)
IndexPeaks(PeaksWorkspace='peaks_81285')
OptimizeLatticeForCellType(PeaksWorkspace='peaks_81285', CellType='Orthorhombic', Apply=True, OutputDirectory='/home/rwp/build/mantid/.')


Load('CORELLI_81300', OutputWorkspace='CORELLI_81300')
SetGoniometer(Workspace='CORELLI_81300', Axis0='BL9:Mot:Sample:Axis3,0,1,0,1')
ConvertToMD(InputWorkspace='CORELLI_81300', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md_81300')



ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_81285:81433:5',
                                     FilterByTofMin=1000,
                                     FilterByTofMax=16666,
                                     MinValues=[-15,-5,-15],
                                     MaxValues=[15,5,15],
                                     OutputWorkspace='output',
                                     SetGoniometer=True,
                                     Axis0="BL9:Mot:Sample:Axis3,0,1,0,1")
FindPeaksMD(InputWorkspace='output', PeakDistanceThreshold=0.5, MaxPeaks=2000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=20)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellWithForm(PeaksWorkspace='peaks', FormNumber=26, Apply=True)
IndexPeaks(PeaksWorkspace='peaks')
SaveIsawPeaks('peaks', Filename='/SNS/users/rwp/corelli/cal_2018_10_Natrolite/peaks_5.peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', CellType='Orthorhombic', Apply=True, OutputDirectory='/SNS/users/rwp/.')
SaveIsawPeaks('peaks', Filename='/SNS/users/rwp/corelli/cal_2018_10_Natrolite/peaks_5_opt.peaks')

# Lattice Parameters:    6.703017   18.304804   18.669009   90.000000   90.000000   90.000000  2290.639063


ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_81285:81433',
                                     FilterByTofMin=1000,
                                     FilterByTofMax=16666,
                                     MinValues=[-15,-5,-15],
                                     MaxValues=[15,5,15],
                                     OutputWorkspace='output',
                                     SetGoniometer=True,
                                     Axis0="BL9:Mot:Sample:Axis3,0,1,0,1")
FindPeaksMD(InputWorkspace='output', PeakDistanceThreshold=0.5, MaxPeaks=2000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=20)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellWithForm(PeaksWorkspace='peaks', FormNumber=26, Apply=True)
IndexPeaks(PeaksWorkspace='peaks')
OptimizeLatticeForCellType(PeaksWorkspace='peaks', CellType='Orthorhombic', Apply=True, OutputDirectory='/SNS/users/rwp/.')

# Lattice Parameters:    6.703017   18.304804   18.669009   90.000000   90.000000   90.000000  2290.639063
