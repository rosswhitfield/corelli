datafile='CORELLI_8064'
cutPoint=4000 #point in TOF separating first and second frame

datafile2=datafile+'_2'

LoadEventNexus('/SNS/CORELLI/IPTS-13204/nexus/'+datafile+'.nxs.h5',OutputWorkspace=datafile)

CropWorkspace(InputWorkspace=datafile,OutputWorkspace=datafile2,Xmin=0,Xmax=cutPoint)
CropWorkspace(InputWorkspace=datafile,OutputWorkspace=datafile,Xmin=cutPoint,Xmax=16667)

ChangeBinOffset(InputWorkspace=datafile2,OutputWorkspace=datafile2,Offset=16667)
ChangePulsetime(InputWorkspace=datafile2,OutputWorkspace=datafile2,TimeOffset=-0.016667)

MergeRuns(InputWorkspaces=[datafile,datafile2],OutputWorkspace=datafile)
DeleteWorkspace(datafile2)

Rebin(InputWorkspace=datafile,OutputWorkspace=datafile,Params=str(cutPoint)+',10,'+str(cutPoint+16670))
