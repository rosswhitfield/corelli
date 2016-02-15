from mantid.simpleapi import *
import numpy as np
import math
import matplotlib.pyplot as plt
from mantid.kernel import V3D

LoadCalFile(InstrumentName='CORELLI', CalFilename='/SNS/users/rwp/cal/c60_5g.cal', MakeGroupingWorkspace=False, MakeMaskWorkspace=False, WorkspaceName='cal')

c=LoadEmptyInstrument(OutputWorkspace='cor',Filename='/SNS/users/rwp/CORELLI_Definition.xml')

#MaskBTP(Workspace='van',Pixel="1-10,246-256")

distance_moderator_sample=c.getInstrument().getComponentByName('moderator').getDistance(c.getInstrument().getSample())

samplePos = c.getInstrument().getSample().getPos()
beamDirection = V3D(0,0,1)

for i in range(30,61): #(30,61)
	p0z=np.zeros(16)
	p1z=np.zeros(16)
	p=0
        x_centre=0
        y_centre=0
        z_centre=0
        n_centre=0
        h_x=np.zeros(16)
        h_y=np.zeros(16)
        h_z=np.zeros(16)
        h_n=0
        v_x=np.zeros(236)
        v_y=np.zeros(236)
        v_z=np.zeros(236)
        h_i=0
	for j in range(i*4096,4096*(i+1)-1,256):
                v_i=0
		for k in range(j+10,j+246):
                    distance_sample_detector=c.getInstrument().getDetector(k).getDistance(c.getInstrument().getSample())
		    scale=((distance_moderator_sample+distance_sample_detector)/distance_sample_detector)*off[k]
		    #print scale
                    x=c.getInstrument().getDetector(k).getPos().getX() *(1-scale)
                    y=c.getInstrument().getDetector(k).getPos().getY() *(1-scale)
                    z=c.getInstrument().getDetector(k).getPos().getZ() *(1-scale)
                    x_centre+=x
                    y_centre+=y
                    z_centre+=z
                    n_centre+=1
                    h_x[h_i]+=x
                    h_y[h_i]+=y
                    h_z[h_i]+=z
                    v_x[v_i]+=x
                    v_y[v_i]+=y
                    v_z[v_i]+=z
                    v_i+=1
                h_i+=1
        #print 'B'+str(i-28),x_centre/n_centre,y_centre/n_centre,z_centre/n_centre
        #print 'h_x',h_x/236
        #print 'h_y',h_y/236
        #print 'h_z',h_z/236
        #print 'v_x',v_x/16
        #print 'v_y',v_y/16
        #print 'v_z',v_z/16
        l=c.getInstrument().getDetector(j+10).getDistance(c.getInstrument().getDetector(j+246))
        #print l
        [Vx,vx0]=np.polyfit(np.linspace(-l/2,l/2,236),v_x,1)
        [Vy,vy0]=np.polyfit(np.linspace(-l/2,l/2,236),v_y,1)
        [Vz,vz0]=np.polyfit(np.linspace(-l/2,l/2,236),v_z,1)
        #print vx1,vy1,vz1
        l=c.getInstrument().getDetector(i*4096+128).getDistance(c.getInstrument().getDetector((i+1)*4096-128))
        #print l
        [Hx,hx0]=np.polyfit(np.linspace(-l/2,l/2,16),h_x,1)
        [Hy,hy0]=np.polyfit(np.linspace(-l/2,l/2,16),h_y,1)
        [Hz,hz0]=np.polyfit(np.linspace(-l/2,l/2,16),h_z,1)
        #print hx1,hy1,hz1
        #print 'H=',hx1,hy1,hz1,'V=',vx1,vy1,vz1
        #print 'B'+str(i-28),'H=',Hx,Hy,Hz,'V=',Vx,Vy,Vz,'Angle=',math.acos((Hx*Vx+Hy*Vy+Hz*Vz)/(math.sqrt(Hx*Hx+Hy*Hy+Hz*Hz)*math.sqrt(Vx*Vx+Vy*Vy+Vz*Vz)))*180/math.pi%180
        Nx=(Hy*Vz-Hz*Vy)
        Ny=-(Hx*Vz-Hz*Vx)
        Nz=(Hx*Vy-Hy*Vz)
        Roty=math.atan2(Nx,Nz)
        Nxy=Nx*math.cos(Roty)-Nz*math.sin(Roty)
        Nyy=Ny
        Nzy=Nx*math.sin(Roty)+Nz*math.cos(Roty)
        Vxy=Vx*math.cos(Roty)-Vz*math.sin(Roty)
        Vyy=Vy
        Vzy=Vx*math.sin(Roty)+Vz*math.cos(Roty)
        Rotx=math.atan2(Nyy,Nzy)
        Nxyx=Nxy*math.cos(Rotx)-Nzy*math.sin(Rotx)
        Nyyx=Nyy
        Nzyx=Nxy*math.sin(Rotx)+Nzy*math.cos(Rotx)
        Vxyx=Vxy*math.cos(Rotx)-Vzy*math.sin(Rotx)
        Vyyx=Vyy
        Vzyx=Vxy*math.sin(Rotx)+Vzy*math.cos(Rotx)
        Rotz=math.atan2(Vxyx,Vyyx)
        print 'B'+str(i-28),2548,0,0,x_centre/n_centre*1000,y_centre/n_centre*1000,z_centre/n_centre*1000,-math.degrees(Rotx),math.degrees(Roty)%360,-math.degrees(Rotz)

