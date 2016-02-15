#CORELLI_7222 293.402517558 Hz 3408.28704648 63000.0ns
#CORELLI_7223 269.875046892 Hz 3705.41853171 65000.0ns
#CORELLI_7224 235.519396056 Hz 4245.93480089 70000.0ns
#CORELLI_7225 214.345054559 Hz 4665.37472514 73000.0ns
#CORELLI_7226 176.698248959 Hz 5659.36564674 81000.0ns
#CORELLI_7227 153.636942268 Hz 6508.85122576 87000.0ns
#CORELLI_7228 111.283332825 Hz 8986.07163011 105000.0ns
#CORELLI_7229 91.5168246345 Hz 10926.9525466 118000.0ns

for run in ((7222,63000),
            #(7223,65000),
            (7224,70000),
            #(7225,73000),
            (7226,81000),
            #(7227,87000),
            #(7228,105000),
            (7229,118000)):
    filename='CORELLI_'+str(run[0])
    LoadEventNexus(Filename='/SNS/CORELLI/IPTS-13328/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
    LoadInstrument(Workspace=filename,InstrumentName='CORELLI')
    CorelliCrossCorrelate(InputWorkspace=filename,OutputWorkspace=filename+'_cc',TimingOffset=str(run[1]))
    ConvertUnits(InputWorkspace=filename, OutputWorkspace=filename+'_d', Target='dSpacing')
    Rebin(InputWorkspace=filename+'_d', OutputWorkspace=filename+'_d', Params='0.02,-0.01,4')
    SumSpectra(InputWorkspace=filename+'_d', OutputWorkspace=filename+'_d')
    ConvertUnits(InputWorkspace=filename+'_cc', OutputWorkspace=filename+'_cc_d', Target='dSpacing')
    Rebin(InputWorkspace=filename+'_cc_d', OutputWorkspace=filename+'_cc_d', Params='0.02,-0.01,4')
    SumSpectra(InputWorkspace=filename+'_cc_d', OutputWorkspace=filename+'_cc_d')
