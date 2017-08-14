w1=Load('CORELLI_29782')
w2=Load('CORELLI_29792')

SetGoniometer(w1,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
SetGoniometer(w2,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")

RemoveLogs(w1, KeepLogs='BL9:Mot:Sample:Axis1')
RemoveLogs(w2, KeepLogs='BL9:Mot:Sample:Axis1')

md=ConvertToMD(w1,QDimensions='Q3D',dEAnalysisMode='Elastic',Q3DFrames='Q_sample',MinValues=[-6,-0.05,0],MaxValues=[-2,0.05,4])
md=ConvertToMD(w2,QDimensions='Q3D',dEAnalysisMode='Elastic',Q3DFrames='Q_sample',MinValues=[-6,-0.05,0],MaxValues=[-2,0.05,4],OverwriteExisting=False)
SaveMD(md,'ConvertMultipleRunsToSingleCrystalMD_QSample.nxs')

LoadIsawUB(w1,"/home/rwp/ConvertMutlipleRunsToSingleCrystalMD/release/ExternalData/Testing/Data/SystemTest/SingleCrystalDiffuseReduction_UB.mat")
LoadIsawUB(w2,"/home/rwp/ConvertMutlipleRunsToSingleCrystalMD/release/ExternalData/Testing/Data/SystemTest/SingleCrystalDiffuseReduction_UB.mat")

md2=ConvertToMD(w1,QDimensions='Q3D',dEAnalysisMode='Elastic',Q3DFrames='HKL',QConversionScales='HKL',MinValues=[-4,3,-0.05],MaxValues=[0,8,0.05])
md2=ConvertToMD(w2,QDimensions='Q3D',dEAnalysisMode='Elastic',Q3DFrames='HKL',QConversionScales='HKL',MinValues=[-4,3,-0.05],MaxValues=[0,8,0.05],OverwriteExisting=False)
SaveMD(md2,'ConvertMultipleRunsToSingleCrystalMD_HKL.nxs')
