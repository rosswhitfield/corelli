ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_29782:29817:10',
                                     SetGoniometer=True,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                                     MinValues='-10,-10,-10',
                                     MaxValues='10,10,10',
                                     OutputWorkspace='md')

FindPeaksMD(InputWorkspace='md',
            DensityThresholdFactor=1000,
            PeakDistanceThreshold=0.5,
            OutputWorkspace='peaks')
    
Load(Filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_29782.nxs.h5', OutputWorkspace='ws')
SetGoniometer('ws',Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
Rebin(InputWorkspace='ws', OutputWorkspace='ws', Params='1')
FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks1')
Rebin(InputWorkspace='ws', OutputWorkspace='ws', Params='10')
FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks2')
FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks3', RangeLower=1000, RangeUpper=16660)
FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks4', RangeLower=4000, RangeUpper=16660)

FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks5', RangeLower=4000, RangeUpper=16660,PeakFindingStrategy="AllPeaks")
FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks6', RangeLower=4000, RangeUpper=16660,PeakFindingStrategy="AllPeaks",AbsoluteBackground=100)
FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks7', RangeLower=4000, RangeUpper=16660,PeakFindingStrategy="AllPeaks",AbsoluteBackground=200)
FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks8', RangeLower=4000, RangeUpper=16660,PeakFindingStrategy="AllPeaks",AbsoluteBackground=400)

for run in range(29782,29817,10):
    Load(Filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_{}.nxs.h5'.format(run), OutputWorkspace='ws')
    SetGoniometer('ws',Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
    Rebin(InputWorkspace='ws', OutputWorkspace='ws', Params='10')
    FindSXPeaks(InputWorkspace='ws', OutputWorkspace='peaks_tmp', RangeLower=4000, RangeUpper=16660,PeakFindingStrategy="AllPeaks",AbsoluteBackground=100)
    if 'peaksCombine' in mtd:
        CombinePeaksWorkspaces(LHSWorkspace='peaksCombine', RHSWorkspace='peaks_tmp',OutputWorkspace= 'peaksCombine')
    else:
        RenameWorkspace('peaks_tmp', 'peaksCombine')
