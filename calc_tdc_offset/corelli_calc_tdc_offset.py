from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt

filename='CORELLI_2257'
bin_size=1

#LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12008/shared/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')
#LoadInstrument(Workspace=filename,Filename='/home/rwp/CORELLI_Definition.xml')
w = mtd[filename]

distance_chopper_to_monitor=w.getInstrument().getComponentByName('correlation-chopper').getDistance(w.getInstrument().getComponentByName('monitor2'))
distance_chopper_to_moderator=w.getInstrument().getComponentByName('correlation-chopper').getDistance(w.getInstrument().getComponentByName('moderator'))
scale=distance_chopper_to_moderator/(distance_chopper_to_moderator+distance_chopper_to_monitor)

ScaleX(InputWorkspace=filename,OutputWorkspace=filename,Factor=str(scale))
Rebin(InputWorkspace=filename,OutputWorkspace=filename,Params=str(bin_size))

chopper_tdc = w.getRun().getProperty("chopper4_TDC").times
sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
chopper_freq = w.getRun().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue()
chopper_per = 1e6/chopper_freq
delay = w.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").timeAverageValue()

print filename,'MotorSpeed =',chopper_freq,'Hz','Chopper period =',chopper_per,'PhaseTimeDelaySet =',delay,'uS'

sequence2=np.append(sequence,sequence)
s=np.cumsum(sequence2)
    
tof=w.getEventList(1).getTofs()
pulse=w.getEventList(1).getPulseTimes()

bins=int(chopper_per/bin_size)+1
x=np.arange(0,chopper_per+bin_size,bin_size)
chopper=np.zeros(bins)

for n in range(bins-1):
    if np.searchsorted(s,((x[n]+x[n+1]) / 2 / chopper_per)*360.)%2==1:
        chopper[n]=1

chopper2 = np.zeros(len(chopper)*2)
chopper2 = np.append(chopper,chopper)

y=np.zeros(bins)
tdc_index=1
print 'Number of monitor events =',len(tof)
for event in range(len(tof)):
    while pulse[event]+int(tof[event]*1000)>chopper_tdc[tdc_index]:
        tdc_index+=1
    y[int(((pulse[event]+int(tof[event]*1000)-chopper_tdc[tdc_index-1]).total_nanoseconds()/bin_size/1000.)%(chopper_per/bin_size))]+=1

corr=np.correlate(y,chopper2)
r=np.argmax(corr)
#r2=(x[r]+x[r+1]) / 2 * 1000
r2=x[r] * 1000

print "Chopper sequence offset = ",r2,"ns"
    
#plt.plot(x[:-1],y)
#plt.plot(x[:-1],np.roll(chopper,r)*y.max()/2)
#plt.show()
