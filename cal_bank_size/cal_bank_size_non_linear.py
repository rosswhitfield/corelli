#!/usr/bin/env python2
import numpy as np
import math as m
from mantid.simpleapi import *
from scipy.optimize import minimize
from scipy.stats import chisquare

#tube_height= 0.88138
#bank_width = 0.20955 # 0.0127*15+0.00127*15
#tube_width = 0.0127

def getPixelPosition(tube, pixel, tube_a=0, tube_b=0.003442890625, tube_c=-0.4389685546875, bank_width=0.20955, x_shift=0, y_shift=0, z_shift=0, alpha=0, beta=0, gamma=0):
    #tube_height=0.88138
    #pixel_width = tube_height / 256
    #y=-tube_height/2+pixel_width/2+pixel_width*pixel
    y=tube_c + tube_b*pixel + tube_a*pixel**2
    x=-bank_width/2+(bank_width/15)*tube
    position=np.matrix([[x],[y],[0]])
    x_rot=np.matrix([
        [1, 0, 0],
        [0, m.cos(m.radians(alpha)), -m.sin(m.radians(alpha))],
        [0, m.sin(m.radians(alpha)),  m.cos(m.radians(alpha))]
    ])
    y_rot=np.matrix([
        [ m.cos(m.radians(beta)), 0, m.sin(m.radians(beta))],
        [0, 1, 0],
        [-m.sin(m.radians(beta)), 0, m.cos(m.radians(beta))]
    ])
    z_rot=np.matrix([
        [m.cos(m.radians(gamma)), -m.sin(m.radians(gamma)), 0],
        [m.sin(m.radians(gamma)),  m.cos(m.radians(gamma)), 0],
        [0, 0, 1]
    ])
    position=y_rot*x_rot*z_rot*position # YXZ
    position[0]=position[0]+x_shift
    position[1]=position[1]+y_shift
    position[2]=position[2]+z_shift
    return position

def calc_difc(position,L1=20.0):
    NeutronMass = 1.674927211e-27
    h = 6.62606896e-34
    constant=2*NeutronMass/h/1e4
    L2=m.sqrt(np.sum(np.power(position,2)))
    twoTheta=m.acos(position[2]/L2)
    difc=constant*m.sin(twoTheta/2)*(L1+L2)
    return difc


# Bank58
p=getPixelPosition(0,128,x_shift=0.228238615,y_shift=0.082562778,z_shift=2.572575854,beta=185.07)
calc_difc(p)

def get_bank_difc(tube_a, tube_b, tube_c, bank_width, x_shift, y_shift, z_shift, alpha, beta, gamma, L1):
    output=[]
    for tube in range(16):
        for pixel in range(256):
            p=getPixelPosition(tube,pixel,tube_a,tube_b,tube_c,bank_width,x_shift,y_shift,z_shift,alpha,beta,gamma)
            output.append(calc_difc(p,L1))
    return np.array(output)

from mantid.simpleapi import *
from scipy.optimize import minimize
from scipy.stats import chisquare

###############################################################################################################

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_C60_20501-8_sum4_mask_lt_3.cal', WorkspaceName='C60')
MaskBTP(Workspace='C60_mask',Pixel="1-16,241-256")
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='corelli')
CalculateDIFC(InputWorkspace='corelli',OutputWorkspace='corelli')

# bank55/B26                                                                                                                            
# B26 2584 1.831 20.28 895.178412 82.562778 2422.580236 0 200.28 0                                                                      
bank=56

firstIndex=16*256*(bank-1)
lastIndex=16*256*bank
new_difc = mtd['C60_cal'].column('difc')[firstIndex:lastIndex]
mask = mtd['C60_mask'].extractY().flatten()[firstIndex:lastIndex]
new_difc = np.ma.masked_array(new_difc, mask)
corelli_difc = np.array(mtd['corelli'].extractY().flatten()[firstIndex:lastIndex])

startPos=mtd['corelli'].getInstrument().getComponentByName('bank'+str(bank)+'/sixteenpack').getPos()
startRot=mtd['corelli'].getInstrument().getComponentByName('bank'+str(bank)+'/sixteenpack').getRotation().getEulerAngles("YXZ")

# All
x0=[0,
    0.003442890625,
    -0.4389685546875,
    0.20955,
    startPos.getX(),
    startPos.getY(),
    startPos.getZ(),
    startRot[1],
    startRot[0],
    startRot[2],
    20.0]

def minimisation_func(x):
    print x
    difc = get_bank_difc(tube_a=x[0], tube_b=x[1], tube_c=x[2], bank_width=x[3],x_shift=x[4],y_shift=x[5],z_shift=x[6],alpha=x[7],beta=x[8],gamma=x[9],L1=x[10])
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, options={'disp': True})

print results

# ta tb tc bw pox poz roty z
x0=[0.0,
    0.003442890625,
    -0.4389685546875,
    0.20955,
    startPos.getX(),
    startPos.getZ(),
    startRot[0],
    20.0]

bnds = ((x0[0]-1,x0[0]+1),
        (x0[1]*0.9,x0[1]*1.1),
        (x0[2]*1.1,x0[2]*0.9),
        (x0[3]*0.9,x0[3]*1.1),
        (x0[4]-0.2,x0[4]+0.2),
        (x0[5]-0.2,x0[5]+0.2),
        (x0[6]-20,x0[6]+20),
        (x0[7]-1,x0[7]+1))

def minimisation_func(x):
    print x
    difc = get_bank_difc(tube_a=x[0], tube_b=x[1], tube_c=x[2], bank_width=x[3],x_shift=x[4],y_shift=0.082562778,z_shift=x[5],alpha=0,beta=x[6],gamma=0,L1=x[7])
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, bounds=bnds, options={'disp': True})

print results

x: array([  3.72962356e-07,   3.44289080e-03,  -4.38968538e-01,
                     2.09549992e-01,   6.77585979e-01,   2.49221114e+00,
                    -1.64790000e+02,   2.00000004e+01])

# bw pox poz roty z
x0=[0.20955,
    startPos.getX(),
    startPos.getZ(),
    startRot[0],
    20.0]

bnds = ((x0[0]*0.9,x0[0]*1.1),
        (x0[1]-0.2,x0[1]+0.2),
        (x0[2]-0.2,x0[2]+0.2),
        (x0[3]-20,x0[3]+20),
        (x0[4]-1,x0[4]+1))

def minimisation_func(x):
    print x
    difc = get_bank_difc(tube_a=0, tube_b=0.003442890625, tube_c=-0.4389685546875, bank_width=x[0],x_shift=x[1],y_shift=0.082562778,z_shift=x[2],alpha=0,beta=x[3],gamma=0,L1=x[4])
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, bounds=bnds, options={'disp': True})

print results

x: array([   0.20171898,    0.64497831,    2.48925754, -159.09477357,   21.        ])


# bw pox poz roty z
x0=[0.20955,
    startPos.getX(),
    startPos.getZ(),
    startRot[0],
    20.0]

bnds = ((x0[0]*0.9,x0[0]*1.1),
        (x0[1]-0.2,x0[1]+0.2),
        (x0[2]-0.2,x0[2]+0.2),
        (x0[3]-20,x0[3]+20),
        (x0[4]-1,x0[4]+1))

def minimisation_func(x):
    print x
    difc = get_bank_difc(tube_a=3.72962356e-07, tube_b=3.44289080e-03, tube_c=-4.38968538e-01, bank_width=x[0],x_shift=x[1],y_shift=0.082562778,z_shift=x[2],alpha=0,beta=x[3],gamma=0,L1=x[4])
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, bounds=bnds, options={'disp': True})

print results
x: array([   0.21032796,    0.67419748,    2.61408818, -159.3682053 ,
             20.99999973])


# ta tb tc pox poz
x0=[0.003442890625,
    -0.4389685546875,
    startPos.getX(),
    startPos.getZ()]

bnds = ((x0[0]*0.9,x0[0]*1.1),
        (x0[1]*1.1,x0[1]*0.9),
        (x0[2]-0.2,x0[2]+0.2),
        (x0[3]-0.2,x0[3]+0.2))

def minimisation_func(x):
    print x
    difc = get_bank_difc(tube_a=0, tube_b=x[0], tube_c=x[1], bank_width=0.20955,x_shift=x[2],y_shift=0.082562778,z_shift=x[3],alpha=0,beta=-164.79,gamma=0,L1=20.0)
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, bounds=bnds, options={'disp': True})

print results


