UB = '/SNS/users/rwp/corelli/FindUB/benzil2.mat'

ConvertMutlipleRunsToSingleCrystalMD(Filename='CORELLI_29533:29535',
                                     OutputWorkspace='output',
                                     SetGoniometer=True,
                                     FilterByTofMin=1000,
                                     FilterByTofMax=17000,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")

ConvertMutlipleRunsToSingleCrystalMD(Filename='CORELLI_29533:29535',
                                     OutputWorkspace='output_ub',
                                     SetGoniometer=True,
                                     Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                                     FilterByTofMin=1000,
                                     FilterByTofMax=17000,
                                     UBMatrix=UB)
