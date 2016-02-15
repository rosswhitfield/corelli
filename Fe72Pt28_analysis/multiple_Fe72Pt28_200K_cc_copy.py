outputdir="/SNS/users/rwp/Fe72Pt28_analysis/"

for i in range(2168,2200):
    filename = "CORELLI_"+str(i)
    data=Load(filename)
    LoadInstrument(data, Filename='/home/rwp/Mantid/mantidgeometry/CORELLI_Definition.xml', MonitorList='-1,-2,-3', RewriteSpectraMap=False)
    data=ChangeBinOffset(data,Offset=500,IndexMin=36864,IndexMax=40959)
    data=ChangeBinOffset(data,Offset=500,IndexMin=45056,IndexMax=53247)
    data=ChangeBinOffset(data,Offset=500,IndexMin=163840,IndexMax=167935)
    data=ChangeBinOffset(data,Offset=500,IndexMin=237568,IndexMax=249855)
    data=Rebin(data,"0,16666,16666")
    data=CorelliCrossCorrelate(data,TimingOffset=56000)
    SaveNexus(data,outputdir+filename+".nxs")
