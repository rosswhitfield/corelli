from mantid.simpleapi import *
import numpy as np
import numpy.ma as ma
from scipy.stats import chisquare
from scipy.optimize import minimize

#offset=LoadNexus(Filename='/home/rwp/AlignBanks/COR_4597_offset.nxs')
offset=LoadNexus(Filename='/home/rwp/AlignBanks/COR_4597_offset_mask.nxs')
MaskBTP(offset,Pixel="1-15,242-256")

#ws=LoadEmptyInstrument(Filename='CORELLI_Definition.xml')

#difc=CalculateDIFC(ws)
mask=ExtractMask(offset)

#difc.extractY()


#calc chi squared

b="B28"

bank=offset.getInstrument().getComponentByName(b+"/sixteenpack")
firstDet=bank[0][0].getID()
lastDet=bank[15][255].getID()

o=offset.extractY().flatten()[firstDet:lastDet+1]
m=mask[1]
m.sort()

mask_array=np.zeros(len(o))
for i in m:
    if i>=firstDet and i<=lastDet:
        mask_array[i-firstDet]=1

om=ma.masked_array(o,mask=mask_array)


difc=CalculateDIFC(offset)
d=difc.extractY().flatten()[firstDet:lastDet+1]

dm=ma.masked_array(d,mask=mask_array)
odm=(1/(1+om))*dm

print "inital chi^2 =",chisquare(f_obs=odm,f_exp=dm)



dm_new=ma.masked_array(difc.extractY().flatten()[firstDet:lastDet+1],mask=mask_array)
print "inital chi^2 =",chisquare(f_obs=odm,f_exp=dm_new)



#MoveInstrumentComponent(ws,'A1/sixteenpack',X=0,Y=0,Z=1,RelativePosition=False)





# ALL
def min_all(x):
    print x
    MoveInstrumentComponent(offset,b,X=x[0],Y=x[1],Z=x[2],RelativePosition=False)
    RotateInstrumentComponent(offset,b+"/sixteenpack",X=1,Y=0,Z=0,Angle=x[3],RelativeRotation=False)
    RotateInstrumentComponent(offset,b+"/sixteenpack",X=0,Y=1,Z=0,Angle=x[4],RelativeRotation=False)
    RotateInstrumentComponent(offset,b+"/sixteenpack",X=0,Y=0,Z=1,Angle=x[5],RelativeRotation=False)
    difc=CalculateDIFC(offset)
    dm_new=ma.masked_array(difc.extractY().flatten()[firstDet:lastDet+1],mask=mask_array)
    print chisquare(f_obs=odm,f_exp=dm_new)
    return chisquare(f_obs=odm,f_exp=dm_new)[0]

x0 = [0.,0.,0.,0.,0.,0.]
bounds = [(-0.1,0.1),(-0.1,0.1),(-0.1,0.1),(-10,10),(-10,10),(-10,10)]
res = minimize(min_all,x0,bounds=bounds)
print res


# Position
def min_position(x):
    print x
    MoveInstrumentComponent(offset,b,X=x[0],Y=x[1],Z=x[2],RelativePosition=False)
    difc=CalculateDIFC(offset)
    dm_new=ma.masked_array(difc.extractY().flatten()[firstDet:lastDet+1],mask=mask_array)
    print chisquare(f_obs=odm,f_exp=dm_new)
    return chisquare(f_obs=odm,f_exp=dm_new)[0]

x0 = [0.,0.,0.]
bounds = [(-0.2,0.2),(-0.2,0.2),(-0.2,0.2)]
res = minimize(min_position,x0,bounds=bounds)
print res


# Rotation
def min_rotation(x):
    print x
    RotateInstrumentComponent(offset,b+"/sixteenpack",X=x[1],Y=x[2],Z=x[3],Angle=x[0],RelativeRotation=False)
    difc=CalculateDIFC(offset)
    dm_new=ma.masked_array(difc.extractY().flatten()[firstDet:lastDet+1],mask=mask_array)
    print chisquare(f_obs=odm,f_exp=dm_new)
    return chisquare(f_obs=odm,f_exp=dm_new)[0]

x0 = [0.,0.,0.]
bounds = [(-10,10),(-10,10),(-10,10)]
res = minimize(min_rotation,x0,bounds=bounds)
print res
