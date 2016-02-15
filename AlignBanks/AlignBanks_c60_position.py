from mantid.simpleapi import *
import numpy as np
import numpy.ma as ma
from scipy.stats import chisquare
from scipy.optimize import minimize

offset=LoadNexus(Filename='/home/rwp/AlignBanks/COR_4597_offset_mask.nxs')
MaskBTP(offset,Pixel="1-15,242-256")

mask=ExtractMask(offset)


bankList = ["B23","B24","B25","B26","B27","B28","B29","B30","B31","B32"]

results=[]

# Position
def min_position(x):
    print x
    MoveInstrumentComponent(offset,b,X=x[0],Y=x[1],Z=x[2],RelativePosition=False)
    difc=CalculateDIFC(offset)
    dm_new=ma.masked_array(difc.extractY().flatten()[firstDet:lastDet+1],mask=mask_array)
    print chisquare(f_obs=odm,f_exp=dm_new)
    return chisquare(f_obs=odm,f_exp=dm_new)[0]

for b in bankList:
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
    x0 = [0.,0.,0.]
    bounds = [(-0.2,0.2),(-0.2,0.2),(-0.2,0.2)]
    res = minimize(min_position,x0,bounds=bounds)
    print res
    results.append(res)


print results
SaveNexus(offset,Filename='/home/rwp/AlignBanks/COR_4597_offset_mask_cal2.nxs')


#Create clean instrument file to save.

output=LoadEmptyInstrument(Filename='/SNS/users/rwp/CORELLI_Definition.xml')

for n in range(len(bankList)):
    x=results[n].values()[4][0]
    y=results[n].values()[4][1]
    z=results[n].values()[4][2]
    MoveInstrumentComponent(output,bankList[n],X=x,Y=y,Z=z,RelativePosition=False)

SaveNexus(output,Filename='/home/rwp/AlignBanks/COR_4597_empty_cal2.nxs')
