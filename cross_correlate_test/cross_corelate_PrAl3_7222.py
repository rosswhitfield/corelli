from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt
import math

filename = 'CORELLI_7222'

ws=LoadEventNexus(Filename=r'/SNS/CORELLI/IPTS-13328/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,BankName='bank42',SingleBankPixelsOnly='0',FilterByTofMin='0',FilterByTofMax='16667')
LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')

sequence = map(float,ws.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
sequence_sum=np.cumsum(sequence)

#i=ws.getInstrument()
#r=i.getDetector(169600).getDistance(i.getSample())

Lmc=17.999347
Lcs=20-Lmc
Lsd=ws.getInstrument().getDetector(168064).getDistance(ws.getInstrument().getSample())
L=Lmc+Lcs+Lsd


chopper_tdc = ws.getSampleDetails().getProperty("chopper4_TDC").times
#chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:SpeedSetReq").value[0]
chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue()
chopper_per = 1e6/chopper_frq

print 'Chopper Frequency =', chopper_frq, 'Hz, Period =', chopper_per, 'uS'

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
            out[int(((chopper_tdc[tdc_index]-pulse[event]).total_microseconds()%chopper_per)/bin_size),int(tofs[event]/bin_size)]+=1




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







np.save(filename+'_out',out)
np.save(filename+'_results',results)



xx=np.linspace(0, x*bin_size, x)
yy=np.linspace(0, y*bin_size, y)
X,Y = np.meshgrid(xx,yy)

fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, out)
cb = fig.colorbar(p, ax=ax)
fig.show()                                                                                       


fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=100)
cb = fig.colorbar(p, ax=ax)
fig.show()                                                                                       


fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=200)
cb = fig.colorbar(p, ax=ax)
plt.plot(xx,((xx*Lmc/L)-50)%chopper_per,color='r')
fig.show()                                                                                       

# +4meV
de=-0.004*1.6e-19
m=1.674927351e-27

yyy=xx*Lmc/L
xxx=yyy+yyy*Lcs/Lmc+Lsd/np.sqrt((Lmc/yyy*1e6)**2+2*de/m)*1e6


fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=200)
cb = fig.colorbar(p, ax=ax)
plt.plot(xx,((xx*Lmc/L)-50)%chopper_per,c='r')
plt.plot(xxx,(yyy-50)%chopper_per,c='r')
fig.show()


fig, ax = plt.subplots(figsize=(14,10))
plt.title(ws.getTitle())
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
plt.xlim([8000,14000])
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=400)
cb = fig.colorbar(p, ax=ax)
p1=plt.plot(xx,((xx*Lmc/L)-50)%chopper_per,c='g')
p2=plt.plot(xxx,(yyy-50)%chopper_per,c='r')
ax.annotate('dE=0meV', xy=(12880,3400), xytext=(13240,3700),arrowprops=dict(facecolor='green',shrink=0.05))
ax.annotate('dE=4meV', xy=(13120,3400), xytext=(13360,3600),arrowprops=dict(facecolor='red',shrink=0.05))
fig.savefig(filename+'_correlated_0-400_a.png')
fig.clf()





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


fig, ax = plt.subplots(figsize=(14,6))
plt.title(filename+' ('+str(chopper_frq)+'Hz)')
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=400)
cb = fig.colorbar(p, ax=ax)
#fig.show()                                                                                                                                                                                                          
fig.savefig(filename+'_correlated_0-400.png')
fig.clf()





fig, ax = plt.subplots(figsize=(14,10))
plt.title(ws.getTitle())
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
plt.xlim([8000,14000])
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=400)
cb = fig.colorbar(p, ax=ax)
                                                                                                                                                                                                                  
fig.savefig(filename+'_correlated_0-400_r.png')
fig.clf()





results[results <=0] =1

fig, ax = plt.subplots(figsize=(14,6))
plt.title(filename+' ('+str(chopper_frq)+'Hz)')
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
p = ax.pcolormesh(X, Y, np.log10(results))
cb = fig.colorbar(p, ax=ax)
#fig.show()                                                                                                                                                                                                          
fig.savefig(filename+'_correlated_log.png')
fig.clf()



fig, ax = plt.subplots(figsize=(14,10))
plt.title(ws.getTitle())
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
plt.xlim([8000,14000])
p = ax.pcolormesh(X, Y, np.log10(results))
cb = fig.colorbar(p, ax=ax)
#fig.show()                                                                                                                                                                                                          
fig.savefig(filename+'_correlated_log_r.png')
fig.clf()

fig, ax = plt.subplots(figsize=(14,10))
plt.title(ws.getTitle())
plt.xlabel('ToF (uS)')
plt.ylabel('Incident ToF (uS)')
plt.xlim([8000,14000])
p = ax.pcolormesh(X, Y, np.log10(results))
cb = fig.colorbar(p, ax=ax)
plt.plot(xx,((xx*Lmc/L)-50)%chopper_per,c='g')
plt.plot(xxx,(yyy-50)%chopper_per,c='r')
ax.annotate('dE=0meV', xy=(12880,3400), xytext=(13240,3700),arrowprops=dict(facecolor='green',shrink=0.05))
ax.annotate('dE=4meV', xy=(13120,3400), xytext=(13360,3600),arrowprops=dict(facecolor='red',shrink=0.05))
#fig.show()                                                                                                                                                                                                          
fig.savefig(filename+'_correlated_0-400_log_a.png')
fig.clf()
