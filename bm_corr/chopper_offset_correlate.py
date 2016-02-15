from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt

def calc_offset(filename,resolution=1,scale=18/(18+0.052),plot=False):
    
    Load(Filename='/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,LoadMonitors='1',MonitorsAsEvents='1')
    LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')
    ScaleX(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Factor=str(scale))
    Rebin(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Params=str(resolution))
    
    w = mtd[filename]
    sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
    freq = round(w.getRun().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue())
    delay = w.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").timeAverageValue()
    
    print filename,'MotorSpeed =',freq,'Hz','PhaseTimeDelaySet =',delay,'uS'
    
    if freq%30 !=0:
        print 'Frequency not a multiple of 30.'
        return
    
    sequence2=sequence
    for i in range(int(freq/60)-1):
        sequence2 = np.append(sequence2,sequence)
    
    m = mtd[filename+'_monitors']
    x=m.extractX()[1]
    y=m.extractY()[1]
    
    s=np.cumsum(sequence2)
    chopper=np.zeros(len(x)-1)
    l=len(chopper)
    
    for n in range(l):
        if np.searchsorted(s,((x[n]+x[n+1]) / 2 / 16666.67)*360.*freq/60.)%2==1:
            chopper[n]=1
            
    chopper2=np.zeros(len(chopper)*2)
    chopper2 = np.append(chopper,chopper)
    
    corr=np.correlate(y,chopper2)
    r=np.argmax(corr)
    r2=(x[r]+x[r+1]) / 2
    
    print "Chopper sequence offset = ",r2,"uS"
    
    chopper=np.roll(chopper,r)
    if plot:
        plt.plot(x[:-1],y)
        plt.plot(x[:-1],chopper*y.max()*0.5)
        plt.show()
    return (freq,delay,r2,corr.max())
