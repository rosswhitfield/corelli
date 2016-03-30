from mantid.simpleapi import *
filename = "/SNS/CORELLI/IPTS-12008/nexus/CORELLI_8196.nxs.h5"

LoadEventNexus(OutputWorkspace='ZrO2',Filename=filename)
SetGoniometer('ZrO2',Axis0="BL9:Mot:Sample:Axis1,0,1,0,1") 
LoadIsawUB(InputWorkspace='ZrO2',Filename="/SNS/CORELLI/IPTS-12008/shared/2015-0411-ZrO2/ZrO2-UB.mat")
RemoveLogs(Workspace='ZrO2')
ConvertToMD(InputWorkspace='ZrO2',OutputWorkspace='MD',QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='1',Uproj='1,0,0',Vproj='0,0,1',Wproj='0,1,0',MinValues='-10.5,0.5,-2.5',MaxValues='0.5,10.5,2.5')
BinMD(InputWorkspace='MD',OutputWorkspace='MDHisto',
                      AlignedDim0="[H,0,0],-10.0,0.0,400",
                      AlignedDim1="[0,0,L],-0.0,10.0,400",
                      AlignedDim2="[0,K,0],-2,2,40")
SaveMD(InputWorkspace='MDHisto',Filename='ZrO2_400_400_40.nxs')
BinMD(InputWorkspace='MD',OutputWorkspace='MDHisto',
                      AlignedDim0="[H,0,0],-5.0,0.0,200",
                      AlignedDim1="[0,0,L],-0.0,10.0,400",
                      AlignedDim2="[0,K,0],0,1,20")
SaveMD(InputWorkspace='MDHisto',Filename='ZrO2_200_400_20.nxs')
BinMD(InputWorkspace='MD',OutputWorkspace='MDHisto',
                      AlignedDim0="[H,0,0],-5.0,0.0,200",
                      AlignedDim1="[0,0,L],-0.0,10.0,200",
                      AlignedDim2="[0,K,0],0.45,0.55,1")
SaveMD(InputWorkspace='MDHisto',Filename='ZrO2_200_200_1.nxs')
ConvertToMD(InputWorkspace='ZrO2',OutputWorkspace='MD',QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                       QConversionScales='HKL',LorentzCorrection='1',Uproj='1,0,0',Vproj='0,0,1',Wproj='0,1,0',MinValues='-10.5,0.5,0.45',MaxValues='0.5,10.5,0.55')
BinMD(InputWorkspace='MD',OutputWorkspace='MDHisto',
                      AlignedDim0="[H,0,0],-5.0,0.0,200",
                      AlignedDim1="[0,0,L],-0.0,10.0,200")
SaveMD(InputWorkspace='MDHisto',Filename='ZrO2_200_200.nxs')
