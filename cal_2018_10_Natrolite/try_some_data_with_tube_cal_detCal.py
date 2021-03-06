import tube
tube.readCalibrationFile('CalibTable','/SNS/users/rwp/corelli/tube_calibration2/CalibTable2_combined.txt')

for run in range(81285,81405+1):
    Load(Filename='CORELLI_{}'.format(run),
         OutputWorkspace='run',
         FilterByTofMin=1000,
         FilterByTofMax=16666)
    SetGoniometer(Workspace='run',
                  Axis0='BL9:Mot:Sample:Axis3,0,1,0,1')
    ApplyCalibration('run','CalibTable')
    LoadIsawDetCal('run','/SNS/users/rwp/corelli/cal_2018_05/a/Aligned3.nxs.detcal')
    ConvertToMD(InputWorkspace='run',
                OutputWorkspace='output',
                QDimensions='Q3D',
                dEAnalysisMode='Elastic',
                Q3DFrames='Q_sample',
                MinValues=[-15,-5,-15],
                MaxValues=[15,5,15],
                OverwriteExisting=False)

FindPeaksMD(InputWorkspace='output', PeakDistanceThreshold=0.5, MaxPeaks=2000, OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks', MinD=5, MaxD=20)
ShowPossibleCells(PeaksWorkspace='peaks')
SelectCellWithForm(PeaksWorkspace='peaks', FormNumber=26, Apply=True)
IndexPeaks(PeaksWorkspace='peaks')


SaveIsawPeaks('peaks', Filename='/SNS/users/rwp/corelli/cal_2018_10_Natrolite/peaks_tubeCal_detCal.peaks')
