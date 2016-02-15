from mantid.simpleapi import *
from mantid.kernel import V3D, UnitConversion, DeltaEModeType
import numpy as np
import matplotlib.pyplot as plt
import math

filename = 'CORELLI_7222'

ws=LoadEventNexus(Filename=r'/SNS/CORELLI/IPTS-13328/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename,FilterByTofMin='3000',FilterByTofMax='16666')
LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')

sequence = map(float,ws.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
sequence_sum=np.cumsum(sequence)


Lmc=17.999347
Lcs=20-Lmc
L1=ws.getInstrument().getSample().getDistance(ws.getInstrument().getSource())

beamDirection = V3D(0,0,1)
samplePos = ws.getInstrument().getSample().getPos()


chopper_tdc = ws.getSampleDetails().getProperty("chopper4_TDC").times
#chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:SpeedSetReq").value[0]
chopper_frq = ws.getSampleDetails().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue()
chopper_per = 1e6/chopper_frq

print 'Chopper Frequency =', chopper_frq, 'Hz, Period =', chopper_per, 'uS'

bin_size=10. # 10ms bins
x_bin_size = 0.02 # A^-1
y = int(math.ceil( chopper_per/bin_size ))
#x = int(math.ceil( 1e6/60/bin_size ))
#out = np.zeros((y,x))
total_counts=0
#results = np.zeros((y,x))

src_unit = "TOF"
dest_unit = "MomentumTransfer"
efixed = 0
emode = DeltaEModeType.Elastic

#UnitConversion.run(src_unit, dest_unit, src_value, l1, l2, twoTheta, emode, efixed)

x = int((UnitConversion.run(src_unit, dest_unit, 3000, L1, ws.getInstrument().getDetector(0).getDistance(ws.getInstrument().getSample()), math.pi , emode, efixed)+1)/x_bin_size)
results = np.zeros((y,x))


for pixelID in range(0,ws.getNumberHistograms(),100): #range(ws.getNumberHistograms())
    L2=ws.getInstrument().getDetector(pixelID).getDistance(ws.getInstrument().getSample())
    twoTheta=ws.getDetector(pixelID).getTwoTheta(samplePos,beamDirection)
    counts=ws.getEventList(pixelID).getNumberEvents()
    total_counts+=counts
    print 'PixelID =',pixelID,'Count at pixel =',counts,'Total counts = ',total_counts,'2Theta = ',twoTheta
    events=ws.getEventList(pixelID)
    n=events.getNumberEvents()
    pulse = events.getPulseTimes()
    tofs = events.getTofs()
    tdc_index=0
    for event in range(n):
        while pulse[event]>chopper_tdc[tdc_index]:
            tdc_index+=1
        yyy=(chopper_tdc[tdc_index]-pulse[event]).total_microseconds()%chopper_per
        x_q=UnitConversion.run(src_unit,dest_unit,tofs[event],L1,L2,twoTheta,emode,efixed)
        xxx=int(x_q/x_bin_size)
        for pk in range(y):
            ij = ((yyy-pk*bin_size)/chopper_per*360.)%360
            if np.searchsorted(sequence_sum,ij)%2==1:
                fact = 0.5
            else:
                fact = -0.5
            results[pk,xxx]+=fact


np.save(filename+'_results_event',results)


xx=np.linspace(0, x*x_bin_size, x)
yy=np.linspace(0, y*bin_size, y)
X,Y = np.meshgrid(xx,yy)

fig, ax = plt.subplots()
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=100)
cb = fig.colorbar(p, ax=ax)
fig.show()                                                                                       
