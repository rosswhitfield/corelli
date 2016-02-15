from mantid.simpleapi import *

IDF="/SNS/users/rwp/new_cal/CORELLI_Definition.xml"

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_14324.nxs.h5', OutputWorkspace='rawSi')
#SetInstrumentParameter(Workspace="rawSi",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
#ModeratorTzero(InputWorkspace="rawSi",OutputWorkspace="rawSi",EMode="Elastic")
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_14325.nxs.h5', OutputWorkspace='rawSi2')
#SetInstrumentParameter(Workspace="rawSi2",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
#ModeratorTzero(InputWorkspace="rawSi2",OutputWorkspace="rawSi2",EMode="Elastic")
LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_14326.nxs.h5', OutputWorkspace='rawSi3')
#SetInstrumentParameter(Workspace="rawSi3",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
#ModeratorTzero(InputWorkspace="rawSi3",OutputWorkspace="rawSi3",EMode="Elastic")

MergeRuns(InputWorkspaces='rawSi, rawSi2, rawSi3',OutputWorkspace='Silicon')
siliconD=ConvertUnits('Silicon',Target='dSpacing')
siliconD=Rebin(InputWorkspace=siliconD,Params='0.5,-0.004,3.5')

#new
LoadInstrument(Workspace="rawSi",Filename=IDF,RewriteSpectraMap=False)
LoadInstrument(Workspace="rawSi2",Filename=IDF,RewriteSpectraMap=False)
LoadInstrument(Workspace="rawSi3",Filename=IDF,RewriteSpectraMap=False)
MergeRuns(InputWorkspaces='rawSi, rawSi2, rawSi3',OutputWorkspace='Silicon_new')
siliconDnew=ConvertUnits('Silicon_new',Target='dSpacing')
siliconDnew=Rebin(InputWorkspace=siliconDnew,Params='0.5,-0.004,3.5')


#group by bank
CreateGroupingWorkspace(InstrumentName='CORELLI', GroupDetectorsBy='bank', OutputWorkspace='group')
GroupDetectors(InputWorkspace='siliconD', OutputWorkspace='siliconDgroup', CopyGroupingFromWorkspace='group')
Rebin(InputWorkspace='siliconDgroup', OutputWorkspace='siliconDgroup', Params='0.0002')
GroupDetectors(InputWorkspace='siliconDnew', OutputWorkspace='siliconDnewgroup', CopyGroupingFromWorkspace='group')
Rebin(InputWorkspace='siliconDnewgroup', OutputWorkspace='siliconDnewgroup', Params='0.0002')



# group by 8
GroupDetectors(InputWorkspace='siliconD', OutputWorkspace='siliconDg8', MapFile='/SNS/users/rwp/new_cal/map8.map')
GroupDetectors(InputWorkspace='siliconDnew', OutputWorkspace='siliconDnewG8', MapFile='/SNS/users/rwp/new_cal/map8.map')
