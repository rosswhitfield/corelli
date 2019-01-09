from mantid import config
config['loading.multifilelimit']='1000'


for run in range(81285,81405+1):

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_81285:81405:5',
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

