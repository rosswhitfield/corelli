from mantid.simpleapi import *
import numpy as np
import numpy.ma as ma
from scipy.stats import chisquare
from scipy.optimize import minimize
import math

offset=LoadNexus(Filename='~/AlignBanks/COR_4597_offset_mask.nxs')
MaskBTP(offset,Pixel="1-15,242-256")

mask=ExtractMask(offset)


bankList = ["B23","B24"]
#bankList = ["B23","B24","B25","B26","B27","B28","B29","B30","B31","B32"]

results=[]

# ALL
def min_all(x):
    print x
    MoveInstrumentComponent(offset,b+"/sixteenpack",X=x[0],Y=x[1],Z=x[2],RelativePosition=False)
    RotateInstrumentComponent(offset,b+"/sixteenpack",X=x[4],Y=x[5],Z=x[6],Angle=x[3],RelativeRotation=False)
    difc=CalculateDIFC(offset)
    dm_new=ma.masked_array(difc.extractY().flatten()[firstDet:lastDet+1],mask=mask_array)
    print chisquare(f_obs=odm,f_exp=dm_new)
    return chisquare(f_obs=odm,f_exp=dm_new)[0]

def quat2wxyz(quat):
    deg=math.acos(quat[0])
    s=math.sin(deg)
    deg*=360.0/math.pi
    x=quat[1]/s
    y=quat[2]/s
    z=quat[3]/s
    return deg,x,y,z

def getRotation(quat):
    aa=quat[1]*quat[1]
    ab=quat[1]*quat[2]
    ac=quat[1]*quat[3]
    aw=quat[1]*quat[0]
    bb=quat[2]*quat[2]
    bc=quat[2]*quat[3]
    bw=quat[2]*quat[0]
    cc=quat[3]*quat[3]
    cw=quat[3]*quat[0]
    out=[]
    out.append(1.0 - 2.0 * (bb + cc))
    out.append(2.0 * (ab - cw))
    out.append(2.0 * (ac + bw))
    out.append(2.0 * (ab + cw))
    out.append((1.0 - 2.0 * (aa + cc)))
    out.append(2.0 * (bc - aw))
    out.append(2.0 * (ac - bw))
    out.append(2.0 * (bc + aw))
    out.append(1.0 - 2.0 * (aa + bb))
    return out

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
    (deg,rotx,roty,rotz)=quat2wxyz(bank.getRotation())
    xi=bank.getPos().getX()
    yi=bank.getPos().getY()
    zi=bank.getPos().getZ()
    x0 = [xi,yi,zi,deg,rotx,roty,rotz]
    bounds = [(xi-0.1,xi+0.1),(yi-0.1,yi+0.1),(zi-0.1,zi+0.1),(max(0,deg-10),min(360,deg+10)),(-0.2,0.2),(0.8,1),(-0.2,0.2)]
    res = minimize(min_all,x0,bounds=bounds)
    print res
    results.append(res)


print results
SaveNexus(offset,Filename='COR_4597_offset_mask_cal3.nxs')


#Create clean instrument file to save.

output=LoadEmptyInstrument(Filename='/SNS/users/rwp/CORELLI_Definition.xml')

for n in range(len(bankList)):
    x=results[n].values()[4][0]
    y=results[n].values()[4][1]
    z=results[n].values()[4][2]
    deg=results[n].values()[4][3]
    rotx=results[n].values()[4][4]
    roty=results[n].values()[4][5]
    rotz=results[n].values()[4][6]
    MoveInstrumentComponent(output,bankList[n],X=x,Y=y,Z=z,RelativePosition=False)
    RotateInstrumentComponent(output,bankList[n]+"/sixteenpack",X=rotx,Y=roty,Z=rotz,Angle=deg,RelativeRotation=False)

SaveNexus(output,Filename='COR_4597_empty_cal3.nxs')

