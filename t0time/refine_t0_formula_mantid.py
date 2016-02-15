from mantid.simpleapi import *
from matplotlib import pyplot as plt
import numpy as np
import math

filename="CORELLI_11005" #120Hz
filename="CORELLI_11004" #60Hz
resolution=1

w=LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
new=ModeratorTzero(w)

w  =Rebin(w,Params='0,'+str(resolution)+',16666')
new=Rebin(new,Params='0,'+str(resolution)+',16666')

x0_old,x1_old,x2_old=w.extractX()
y0_old,y1_old,y2_old=w.extractY()
x0_new,x1_new,x2_new=new.extractX()
y0_new,y1_new,y2_new=new.extractY()

plt.plot(x1_old[:-1],y1_old)
plt.plot(x1_new[:-1],y1_new)
plt.show()

plt.plot(x2_old[:-1],y2_old)
plt.plot(x2_new[:-1],y2_new)
plt.show()




source = w.getInstrument().getSource()
distanceMtoM3 = source.getDistance(w.getInstrument().getComponentByName("monitor3"))
distanceMtoM2 = source.getDistance(w.getInstrument().getComponentByName("monitor2"))

scale=distanceMtoM3/distanceMtoM2

scaled=ScaleX(new,Factor=scale)
x0_scaled,x1_scaled,x2_scaled=scaled.extractX()
y0_scaled,y1_scaled,y2_scaled=scaled.extractY()

plt.plot(x2_new[:-1],y2_new)
plt.plot(x1_scaled[:-1],y1_scaled)
plt.show()

SetInstrumentParameter(w,ParameterName="t0_formula",Value="100")
new2=ModeratorTzero(w)
x0_new2,x1_new2,x2_new2=new2.extractX()
y0_new2,y1_new2,y2_new2=new2.extractY()
scaled2=ScaleX(new2,Factor=scale)
x0_scaled2,x1_scaled2,x2_scaled2=scaled2.extractX()
y0_scaled2,y1_scaled2,y2_scaled2=scaled2.extractY()
plt.plot(x2_new[:-1],y2_new,label="old")
plt.plot(x2_new2[:-1],y2_new2,label="new")
plt.plot(x1_scaled[:-1],y1_scaled,label="old scaled")
plt.plot(x1_scaled2[:-1],y1_scaled2,label="new scaled")
plt.legend()
plt.show()


def min_func(x):
    SetInstrumentParameter(w,ParameterName="t0_formula",Value=str(x))
    new2=ModeratorTzero(w)
    new2_scaled=ScaleX(new2,Factor=scale)
    new2=Rebin(new2,Params='3700,'+str(resolution)+',16600')
    new2_scaled=Rebin(new2_scaled,Params='3700,'+str(resolution)+',16600')
    y0_new2,y1_new2,y2_new2=new2.extractY()
    y0_new2_scaled,y1_new2_scaled,y2_new2_scaled=new2_scaled.extractY()
    

plt.plot(y2_new2)
plt.plot(y2_new2_scaled)
plt.show()
