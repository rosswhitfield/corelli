from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal


def calc_offset(filename,resolution=1,scale=1.0,plot=False):
    
    Load(Filename='/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,LoadMonitors='1',MonitorsAsEvents='1')
    LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')
    ScaleX(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Factor=str(scale))
    Rebin(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Params=str(resolution))
    
    w = mtd[filename]
    sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
    freq = round(w.getRun().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue())
    delay = w.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").timeAverageValue()
    
    print filename,'MotorSpeed =',freq,'Hz','PhaseTimeDelaySet =',delay,'uS'
    
    if freq%60 !=0:
        print 'Frequency not a multiple of 60.'
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
    
    #y=np.roll(chopper,1337)
    
    corr=np.correlate(y,chopper2)
    r=np.argmax(corr)
    r2=(x[r]+x[r+1]) / 2
    
    #print x[-1]
    print "Chopper sequence offset = ",r2,"uS"
    
    chopper=np.roll(chopper,r)
    if plot:
        plt.plot(x[:-1],y)
        plt.plot(x[:-1],chopper*y.max()*0.5)
        plt.show()
    return (freq,delay,r2,corr.max())



def calc_offset_plot(filename,resolution=1,scale=1.0):
    
    Load(Filename='/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,LoadMonitors='1',MonitorsAsEvents='1')
    LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')
    ScaleX(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Factor=str(scale))
    Rebin(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Params=str(resolution))
    
    w = mtd[filename]
    sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
    freq = round(w.getRun().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue())
    delay = w.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").timeAverageValue()
    
    print filename,'MotorSpeed =',freq,'Hz','PhaseTimeDelaySet =',delay,'uS'
    
    if freq%60 !=0:
        print 'Frequency not a multiple of 60.'
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
    
    #y=np.roll(chopper,1337)
    
    corr=np.correlate(y,chopper2)
    r=np.argmax(corr)
    r2=(x[r]+x[r+1]) / 2
    
    #print x[-1]
    print "Chopper sequence offset = ",r2,"uS"
    
    chopper=np.roll(chopper,r)
    
    chopper[0]=0
    chopper[-1]=0
    
    lb=2500
    ub=13500
    fig = plt.figure(1,figsize=(14,6))
    plt.title(filename+' ('+str(freq)+'Hz)')
    #plt.plot(x[lb:ub],y[lb:ub])
    #plt.plot(x[lb:ub],chopper[lb:ub]*y.max()*0.5)
    plt.plot(x[:-1],y)
    plt.plot(x[:-1],chopper*y.max()*0.5)
    plt.xlabel('ToF (uS)')
    plt.xlim([lb,ub])
    fig.savefig('/SNS/users/rwp/'+filename+'.png')
    fig.clf()

    #chopper[lb]=0.0
    #chopper[ub-1]=0.0
    fig = plt.figure(1,figsize=(14,6))
    plt.title(filename+' ('+str(freq)+'Hz)')
    #plt.fill(x[lb:ub],chopper[lb:ub]*y.max(),color = '0.85')
    #plt.plot(x[lb:ub],y[lb:ub])
    plt.fill(x[:-1],chopper*y.max(),color = '0.85')
    plt.plot(x[:-1],y)
    plt.xlabel('ToF (uS)')
    plt.xlim([lb,ub])
    fig.savefig('/SNS/users/rwp/'+filename+'_fill.png')
    fig.clf()
    
    lb=5000
    ub=8000
    fig = plt.figure(1,figsize=(14,6))
    plt.title(filename+' ('+str(freq)+'Hz)')
    plt.plot(x[:-1],y)
    plt.plot(x[:-1],chopper*y.max()*0.5)
    plt.xlabel('ToF (uS)')
    plt.xlim([lb,ub])
    fig.savefig('/SNS/users/rwp/'+filename+'_2.png')
    fig.clf()

    #chopper[lb]=0.0
    #chopper[ub-1]=0.0
    fig = plt.figure(1,figsize=(14,6))
    plt.title(filename+' ('+str(freq)+'Hz)')
    plt.fill(x[:-1],chopper*y.max(),color = '0.85')
    plt.plot(x[:-1],y)
    plt.xlabel('ToF (uS)')
    plt.xlim([lb,ub])
    fig.savefig('/SNS/users/rwp/'+filename+'_fill_2.png')
    fig.clf()
    
    Rebin(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Params='5')
    Load(Filename=r'/SNS/CORELLI/IPTS-12008/nexus/CORELLI_306.nxs.h5',OutputWorkspace='CORELLI_306',LoadMonitors='1',MonitorsAsEvents='1')
    ScaleX(InputWorkspace='CORELLI_306_monitors',OutputWorkspace='CORELLI_306_monitors',Factor=str(scale))
    Rebin(InputWorkspace='CORELLI_306_monitors',OutputWorkspace='CORELLI_306_monitors',Params='5')
    Divide(LHSWorkspace=filename+'_monitors',RHSWorkspace='CORELLI_306_monitors',OutputWorkspace='out',WarnOnZeroDivide='0')
    norm = mtd['out']
    #ox=norm.extractX()[1]
    #oy=norm.extractY()[1]
    
    #lb=3000
    #ub=13000
    #fig = plt.figure(1,figsize=(14,6))
    #plt.title(filename+' ('+str(freq)+'Hz) Normalized')
    #plt.fill(x[lb:ub],chopper[lb:ub]*y[lb:ub].max(),color = '0.85')
    #plt.plot(ox[lb:ub],oy[lb:ub])
    #plt.xlabel('ToF (uS)')
    #plt.xlim([lb,ub])
    #fig.savefig('/SNS/users/rwp/'+filename+'_norm.png')
    #fig.clf()
    
    
    
    #return (freq,delay,r2,corr.max())
    return (x,y,chopper)

def calc_offset_plot_norm(filename,resolution=1,scale=1.0):
    
    Load(Filename=r'/SNS/CORELLI/IPTS-12008/nexus/CORELLI_306.nxs.h5',OutputWorkspace='CORELLI_306',LoadMonitors='1',MonitorsAsEvents='1')
    Load(Filename=r'/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,LoadMonitors='1',MonitorsAsEvents='1')
    ScaleX(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Factor=str(scale))
    ScaleX(InputWorkspace='CORELLI_306_monitors',OutputWorkspace='CORELLI_306_monitors',Factor=str(scale))
    Rebin(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Params='5')
    Rebin(InputWorkspace='CORELLI_306_monitors',OutputWorkspace='CORELLI_306_monitors',Params='5')
    Divide(LHSWorkspace=filename+'_monitors',RHSWorkspace='CORELLI_306_monitors',OutputWorkspace='out',WarnOnZeroDivide='0')
    
    #Load(Filename='/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,LoadMonitors='1',MonitorsAsEvents='1')
    #LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')
    #ScaleX(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Factor=str(scale))
    #Rebin(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Params=str(resolution))

    LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')

    
    w = mtd[filename]
    sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
    freq = round(w.getRun().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue())
    delay = w.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").timeAverageValue()
    
    print filename,'MotorSpeed =',freq,'Hz','PhaseTimeDelaySet =',delay,'uS'
    
    if freq%60 !=0:
        print 'Frequency not a multiple of 60.'
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
    
    #y=np.roll(chopper,1337)
    
    corr=np.correlate(y,chopper2)
    r=np.argmax(corr)
    r2=(x[r]+x[r+1]) / 2
    
    #print x[-1]
    print "Chopper sequence offset = ",r2,"uS"
    
    chopper=np.roll(chopper,r)
    
    chopper[0]=0
    chopper[-1]=0

    norm = mtd['out']
    x=norm.extractX()[1]
    y=norm.extractY()[1]
    
    lb=3000
    ub=13000
    
    fig = plt.figure(1,figsize=(14,6))
    plt.title(filename+' ('+str(freq)+'Hz) Normalized')
    plt.plot(x[:-1],y)
    plt.plot(x[:-1],chopper*y[1000:1600].max())
    plt.xlabel('ToF (uS)')
    plt.xlim([lb,ub])
    fig.savefig('/SNS/users/rwp/'+filename+'_norm.png')
    fig.clf()

    lb=5000
    ub=8000
    
    fig = plt.figure(1,figsize=(14,6))
    plt.title(filename+' ('+str(freq)+'Hz) Normalized')
    plt.plot(x[:-1],y)
    plt.plot(x[:-1],chopper*y[1000:1600].max())
    plt.xlabel('ToF (uS)')
    plt.xlim([lb,ub])
    fig.savefig('/SNS/users/rwp/'+filename+'_norm_2.png')
    fig.clf()
    
    #return (freq,delay,r2,corr.max())
    #return (x,y,chopper)
