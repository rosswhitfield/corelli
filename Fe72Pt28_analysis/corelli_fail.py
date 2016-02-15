outputdir="/SNS/users/rwp/Fe72Pt28_analysis/"

filename = "CORELLI_2168"
data=Load(filename)
#data=ChangeBinOffset(data,Offset=500,IndexMin=237568,IndexMax=249855)
data=ChangeBinOffset(data,Offset=500,IndexMin=0,IndexMax=25000)
data=Rebin(data,'0,16666,16666')
#data=CropWorkspace(data,0,16666)
#LoadInstrument(data, Filename='/home/rwp/Mantid/mantidgeometry/CORELLI_Definition.xml', MonitorList='-1,-2,-3', RewriteSpectraMap=False)
#data=CorelliCrossCorrelate(data,TimingOffset=56000)
SaveNexus(Filename=outputdir+filename+'.nxs',InputWorkspace=data)
LoadNexus(Filename=outputdir+filename+'.nxs',OutputWorkspace="ws")
