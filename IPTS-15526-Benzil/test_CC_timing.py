LoadEventNexus(OutputWorkspace='ws',Filename="CORELLI_29827")

for t in range(50000,63000,2000):
    new_ws='timing_'+str(t)
    CorelliCrossCorrelate(InputWorkspace='ws',OutputWorkspace=new_ws,TimingOffset=t)
    ConvertUnits(InputWorkspace=new_ws, OutputWorkspace=new_ws, Target='dSpacing')
    Rebin(InputWorkspace=new_ws, OutputWorkspace=new_ws, Params='0.1,-0.005,10')
    SumSpectra(InputWorkspace=new_ws, OutputWorkspace=new_ws)
