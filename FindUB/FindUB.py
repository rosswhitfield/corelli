from mantid.simpleapi import Load, ConvertToMD, FindPeaksMD, FindUBUsingFFT, IndexPeaks, SetGoniometer

files = ['CORELLI_'+str(run) for run in range(29782,29817,10)]

max_Q = "30"

num_peaks_to_find = 400

min_d = 8
max_d = 20
tolerance = 0.12

minVals = "-"+max_Q +",-"+max_Q +",-"+max_Q
maxVals = max_Q +","+max_Q +","+ max_Q

distance_threshold = 0.9 * 6.28 / float(max_d)

for f in files:
    data = Load(f)
    SetGoniometer(data,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
    MDEW = ConvertToMD(InputWorkspace=data, QDimensions="Q3D",
                       dEAnalysisMode="Elastic", QConversionScales="Q in A^-1",
                       LorentzCorrection='0', MinValues=minVals, MaxValues=maxVals,
                       SplitInto='2', SplitThreshold='50',MaxRecursionDepth='11')
    peaks_ws = FindPeaksMD(MDEW, MaxPeaks=num_peaks_to_find,
                           PeakDistanceThreshold=distance_threshold,
                           AppendPeaks=True)

FindUBUsingFFT( PeaksWorkspace=peaks_ws, MinD=min_d, MaxD=max_d, Tolerance=tolerance )
IndexPeaks( PeaksWorkspace=peaks_ws, Tolerance=tolerance)
#SaveIsawUB( InputWorkspace=peaks_ws,Filename=run_niggli_matrix_file )
