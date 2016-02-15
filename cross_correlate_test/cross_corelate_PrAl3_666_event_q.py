from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt
import math

filename = 'CORELLI_666'

ws=LoadEventNexus(Filename=r'/SNS/CORELLI/IPTS-12008/shared/SNS/CORELLI/IPTS-12008/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,BankName='bank42',SingleBankPixelsOnly='0',FilterByTofMin='0',FilterByTofMax='16667')
LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')

sequence = map(float,ws.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
sequence_sum=np.cumsum(sequence)

#i=ws.getInstrument()
#r=i.getDetector(169600).getDistance(i.getSample())

Lmc=17.999347
Lcs=20-Lmc


chopper_tdc = ws.getSampleDetails().getProperty("chopper4_TDC").times
#chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:SpeedSetReq").value[0]
chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue()
chopper_per = 1e6/chopper_frq

print 'Chopper Frequency =', chopper_frq, 'Hz, Period =', chopper_per, 'uS'

bin_size=10. # 10ms bins
y = int(math.ceil( chopper_per/bin_size ))
x = int(math.ceil( 1e6/60/bin_size ))
#out = np.zeros((y,x))
total_counts=0
results = np.zeros((y,x))

for pi in range(0,1): #4
    for pj in range(0,1): #16
        pixelID = 167936+256*pi+120+pj 
        Lsd=ws.getInstrument().getDetector(pixelID).getDistance(ws.getInstrument().getSample())
        L=Lmc+Lcs+Lsd
        counts=ws.getEventList(pixelID).getNumberEvents()
        total_counts+=counts
        print 'PixelID =',pixelID,'Count at pixel =',counts,'Total counts = ',total_counts
        events=ws.getEventList(pixelID)
        n=events.getNumberEvents()
        pulse = events.getPulseTimes()
        tofs = events.getTofs()
        tdc_index=0
        for event in range(n):
            #print event
            while pulse[event]>chopper_tdc[tdc_index]:
                tdc_index+=1
            #out[int(((chopper_tdc[tdc_index]-pulse[event]).total_microseconds()%chopper_per)/bin_size),int(tofs[event]/bin_size)]+=1
            yyy=(chopper_tdc[tdc_index]-pulse[event]).total_microseconds()%chopper_per
            xxx=int(tofs[event]/bin_size)
            for pk in range(y):
                ij = ((yyy-pk*bin_size)/chopper_per*360.)%360
                if np.searchsorted(sequence_sum,ij)%2==1:
                    fact = 0.5
                else:
                    fact = -0.5
                results[pk,xxx]+=fact


np.save(filename+'_results_event',results)


xx=np.linspace(0, x*bin_size, x)
yy=np.linspace(0, y*bin_size, y)
X,Y = np.meshgrid(xx,yy)

fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=100)
cb = fig.colorbar(p, ax=ax)
fig.show()                                                                                       
