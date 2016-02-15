from mantid.simpleapi import *

IDF="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml"

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_4597.nxs.h5', OutputWorkspace='COR_4597')
c60=ConvertUnits('COR_4597',Target='dSpacing')
c60=Rebin(InputWorkspace=c60,Params='0.5,-0.004,10.0')

LoadInstrument(Workspace="COR_4597",Filename=IDF,RewriteSpectraMap=False)
SetInstrumentParameter(Workspace="COR_4597",ParameterName="t0_formula",Value="(23.5 * exp(-incidentEnergy/205.8))")
ModeratorTzero(InputWorkspace="COR_4597",OutputWorkspace="COR_4597",EMode="Elastic")
c60t=ConvertUnits('COR_4597',Target='dSpacing')
c60t=Rebin(InputWorkspace=c60t,Params='0.5,-0.004,10.0')




# test

IDF="/SNS/users/rwp/new_cal/CORELLI_Definition.xml"

LoadEventNexus(Filename='/SNS/CORELLI/IPTS-12310/nexus/CORELLI_4597.nxs.h5', OutputWorkspace='COR_4597')
c60=ConvertUnits('COR_4597',Target='dSpacing')
c60=Rebin(InputWorkspace=c60,Params='0.5,-0.004,10.0')

LoadInstrument(Workspace="COR_4597",Filename=IDF,RewriteSpectraMap=False)
c60new=ConvertUnits('COR_4597',Target='dSpacing')
c60new=Rebin(InputWorkspace=c60new,Params='0.5,-0.004,10.0')

CreateGroupingWorkspace(InstrumentName='CORELLI', GroupDetectorsBy='bank', OutputWorkspace='group')
GroupDetectors(InputWorkspace='c60', OutputWorkspace='c60group', CopyGroupingFromWorkspace='group')
Rebin(InputWorkspace='c60group', OutputWorkspace='c60group', Params='0.0002')
GroupDetectors(InputWorkspace='c60new', OutputWorkspace='c60newgroup', CopyGroupingFromWorkspace='group')
Rebin(InputWorkspace='c60newgroup', OutputWorkspace='c60newgroup', Params='0.0002')
