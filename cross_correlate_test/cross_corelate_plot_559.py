filename = 'CORELLI_551'
filename = 'CORELLI_552'
filename = 'CORELLI_553'
filename = 'CORELLI_554'
filename = 'CORELLI_555'
filename = 'CORELLI_556'
filename = 'CORELLI_557'
filename = 'CORELLI_558'
filename = 'CORELLI_559'
filename = 'CORELLI_560'
filename = 'CORELLI_561'
filename = 'CORELLI_562'
filename = 'CORELLI_563'


from mantid.simpleapi import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

ws=LoadEventNexus(Filename='/SNS/CORELLI/shared/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,BankName='bank42',SingleBankPixelsOnly='0')
LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')

sequence = map(float,ws.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
sequence_sum=np.cumsum(sequence)

i=ws.getInstrument()
r=i.getDetector(169600).getDistance(i.getSample())

chopper_tdc = ws.getSampleDetails().getProperty("chopper4_TDC").times
chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:SpeedSetReq").value[0]
chopper_per = 1e6/chopper_frq

print 'File =',filename,'Chopper Frequency =', chopper_frq, 'Hz, Period =', chopper_per, 'uS'

bin_size=10. # 10ms bins
y = int(math.ceil( chopper_per/bin_size ))
x = int(math.ceil( 1e6/60/bin_size ))
out = np.zeros((y,x))
total_counts=0


for pi in range(0,4): #4
    for pj in range(0,16): #16
        pixelID = 167936+256*pi+120+pj
        counts=ws.getEventList(pixelID).getNumberEvents()
        total_counts+=counts
        print 'PixelID =',pixelID,'Count at pixel =',counts,'Total counts = ',total_counts
        events=ws.getEventList(pixelID)
        n=events.getNumberEvents()
        pulse = events.getPulseTimes()
        tofs = events.getTofs()
        tdc_index=0
        for event in range(n):
            while pulse[event]>chopper_tdc[tdc_index]:
                tdc_index+=1
            #print pulse[event],tofs[event],tdc_index,chopper_tdc[tdc_index],(pulse[event]-chopper_tdc[tdc_index]).total_microseconds()
            out[int(((chopper_tdc[tdc_index]-pulse[event]).total_microseconds()%chopper_per)/10),int(tofs[event]/10)]+=1




results = np.zeros((y,x))
for pi in range(y):
    print pi
    for pj in range(y):
        ij = ((pi-pj)/chopper_per*3600.)%360
        if np.searchsorted(sequence_sum,ij)%2==1:
            fact = 0.5
        else:
            fact = -0.5
        #print pi,pj,ij,fact
        for pk in range(x):
            results[pi,pk]+=fact*out[pj,pk]






xx=np.linspace(0, x*bin_size, x)
yy=np.linspace(0, y*bin_size, y)
X,Y = np.meshgrid(xx,yy)

fig, ax = plt.subplots(figsize=(14,6))
plt.title(filename+' ('+str(chopper_frq)+'Hz)')
plt.xlabel('ToF (uS)')
plt.ylabel('Chopper Offset (uS)')
p = ax.pcolormesh(X, Y, out)
cb = fig.colorbar(p, ax=ax)
#fig.show()
fig.savefig(filename+'.png')
fig.clf()

fig, ax = plt.subplots(figsize=(14,6))
plt.title(filename+' ('+str(chopper_frq)+'Hz)')
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
p = ax.pcolormesh(X, Y, results)
cb = fig.colorbar(p, ax=ax)
#fig.show()
fig.savefig(filename+'_correlated.png')
fig.clf()

fig, ax = plt.subplots(figsize=(14,6))
plt.title(filename+' ('+str(chopper_frq)+'Hz)')
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
p = ax.pcolormesh(X, Y, results, vmin=0)
cb = fig.colorbar(p, ax=ax)
#fig.show()
fig.savefig(filename+'_correlated_0.png')
fig.clf()
