ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_29782:29817:10',
                                     OutputWorkspace='output',
                                     SetGoniometer=True,
                                     FilterByTofMin=1000,
                                     FilterByTofMax=17000,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")

ConvertMultipleRunsToSingleCrystalMD(Filename='CORELLI_29782:29817:10',
                                     OutputWorkspace='output_ub',
                                     SetGoniometer=True,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                                     FilterByTofMin=1000,
                                     FilterByTofMax=17000,
                                     UBMatrix='/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat')

