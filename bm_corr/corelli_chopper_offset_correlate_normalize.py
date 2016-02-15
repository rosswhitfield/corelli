from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt
#from scipy import signal

filename = 'CORELLI_317'

Load(Filename='/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,LoadMonitors='1',MonitorsAsEvents='1')
Load(Filename='/SNS/CORELLI/IPTS-12008/nexus/CORELLI_306.nxs.h5',OutputWorkspace="CORELLI_306",LoadMonitors='1',MonitorsAsEvents='1')
Rebin(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Params='1')
Rebin(InputWorkspace='CORELLI_306_monitors',OutputWorkspace='CORELLI_306_monitors',Params='1')

Divide(LHSWorkspace='CORELLI_317_monitors',RHSWorkspace='CORELLI_306_monitors',OutputWorkspace='CORELLI_317_monitors',WarnOnZeroDivide='0')

LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')



w = mtd[filename]
sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())

m = mtd[filename+'_monitors']
x=m.extractX()[1]
y=m.extractY()[1]

s=np.cumsum(sequence)
chopper=np.zeros(len(x)-1)
l=len(chopper)

for n in range(l):
    if np.searchsorted(s,((x[n]+x[n+1]) / 2 / x[-1])*360.)%2==1:
        chopper[n]=1

chopper2=np.zeros(len(chopper)*2)
chopper2[0:l]=chopper
chopper2[l:l*2]=chopper

#y=np.roll(chopper,1337)

r=np.argmax(np.correlate(y,chopper2))
r2=(x[r]+x[r+1]) / 2

print "Chopper sequence offset = ",r2,"uS"

chopper=np.roll(chopper,r)

plt.plot(x[:-1],y)
plt.plot(x[:-1],chopper)
plt.show()
