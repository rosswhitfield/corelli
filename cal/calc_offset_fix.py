from mantid.simpleapi import *
import numpy as np
import math
import matplotlib.pyplot as plt

offset=LoadNexus(Filename='/SNS/users/rwp/COR_525_offset.nxs', OutputWorkspace='offset')
off=offset.extractY().flatten()

c=LoadEmptyInstrument(OutputWorkspace='cor',Filename='/SNS/users/rwp/CORELLI_Definition.xml')
#c=LoadEmptyInstrument(OutputWorkspace='cor',Filename='/home/rwp/CORELLI_Definition.xml')

#MaskBTP(Workspace='van',Pixel="1-10,246-256")

for i in range(30,61):
    for j in range(i*4096,4096*(i+1)-1,256):
        #print off[j:j+256]
        print i,j,'B'+str(i-28)

i=41
p0z=np.zeros(16)
p1z=np.zeros(16)
p=0
for j in range(i*4096,4096*(i+1)-1,256):
    x=np.arange(-118,118)
    [p1,p0]=np.polyfit(x,off[j+10:j+246],1)
    p0z[p]=p0
    p1z[p]=p1
    p+=1
    plt.plot(x,off[j+10:j+246])
    plt.plot(x,x*p1+p0)
    print j,p0,p1

#c.getInstrument().getDetector(100000).getPos()
#c.getInstrument().getDetector(100000).getDistance(c.getInstrument().getSample())

for i in range(30,61):
	p0z=np.zeros(16)
	p1z=np.zeros(16)
	p=0
	for j in range(i*4096,4096*(i+1)-1,256):
		l=c.getInstrument().getDetector(j+10).getDistance(c.getInstrument().getDetector(j+246))
		#x=np.arange(-118,118)
		#[p1,p0]=np.polyfit(x,off[j+10:j+246],1)
		x=np.linspace(-l/2,l/2,236)
		y=np.zeros(236)
		n=0
		for k in range(j+10,j+246):
			y[n]=c.getInstrument().getDetector(k).getDistance(c.getInstrument().getSample())#*(1+off[k])
			n+=1
		[p1,p0]=np.polyfit(x,y,1)
		p0z[p]=p0
		p1z[p]=p1
		p+=1
		#print x,y
		#print i,j,p0,p1,l
	#[p0zp1,p0zp0]=np.polyfit(range(0,16),p0z,1)
	#[p1zp1,p1zp0]=np.polyfit(range(0,16),p1z,1)
	#print 'B'+str(i-28),i,np.mean(p0z),np.mean(p1z),p0zp0,p0zp1,p1zp0,p1zp1
	print 'B'+str(i-28),i,np.mean(p0z),np.mean(p1z)
