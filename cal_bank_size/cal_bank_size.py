#!/usr/bin/env python2
import numpy as np
import math as m
from mantid.simpleapi import *
from scipy.optimize import minimize
from scipy.stats import chisquare

#tube_height= 0.88138
#bank_width = 0.20955 # 0.0127*15+0.00127*15
#tube_width = 0.0127

def getPixelPosition(tube, pixel, tube_height=0.88138, bank_width=0.20955, x_shift=0, y_shift=0, z_shift=0, alpha=0, beta=0, gamma=0):
    pixel_width = tube_height / 256
    x=-bank_width/2+(bank_width/15)*tube
    y=-tube_height/2+pixel_width/2+pixel_width*pixel
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

def get_bank_difc(tube_height, bank_width, x_shift, y_shift, z_shift, alpha, beta, gamma, L1):
    output=[]
    for tube in range(16):
        for pixel in range(256):
            p=getPixelPosition(tube,pixel,tube_height,bank_width,x_shift,y_shift,z_shift,alpha,beta,gamma)
            output.append(calc_difc(p,L1))
    return np.array(output)

from mantid.simpleapi import *
firstIndex=233472
lastIndex=237568
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='corelli')
CalculateDIFC(InputWorkspace='corelli',OutputWorkspace='corelli')
corelli_difc = np.array(mtd['corelli'].extractY().flatten()[firstIndex:lastIndex])

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_19284_19285_sum4.cal', WorkspaceName='Si')
MaskBTP(Workspace='Si_mask',Pixel="1-16,241-256")
mask = mtd['Si_mask'].extractY().flatten()[firstIndex:lastIndex]
new_difc = mtd['Si_cal'].column('difc')[firstIndex:lastIndex]
new_difc = np.ma.masked_array(new_difc, mask)

from scipy.optimize import minimize
from scipy.stats import chisquare


# Refine all
x_0=[0.88138,0.20955,0.228238615,0.082562778,2.572575854,0,185.07,0,20.0]
def minimisation_func(x):
    #difc = get_bank_difc(tube_height=0.88138, bank_width=0.20955,x_shift=0.228238615,y_shift=0.082562778,z_shift=2.572575854,alpha=0,beta=185.07,gamma=0,L1=20.0)
    print x
    difc = get_bank_difc(tube_height=x[0], bank_width=x[1],x_shift=x[2],y_shift=x[3],z_shift=x[4],alpha=x[5],beta=x[6],gamma=x[7],L1=x[8])
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]


results = minimize(minimisation_func, x0=x_0, options={'disp': True})


# Refine height, width, x, z, gamma
x0=[0.88138,0.20955,0.228238615,2.572575854,185.07]
bnds = ((x0[0]-0.2,x0[0]+0.2),
        (x0[1]-0.2,x0[1]+0.2),
        (x0[2]-0.2,x0[2]+0.2),
        (x0[3]-0.2,x0[3]+0.2),
        (x0[4]-20,x0[4]+20))
def minimisation_func(x):
    #difc = get_bank_difc(tube_height=0.88138, bank_width=0.20955,x_shift=0.228238615,y_shift=0.082562778,z_shift=2.572575854,alpha=0,beta=185.07,gamma=0,L1=20.0)
    print x
    difc = get_bank_difc(tube_height=x[0], bank_width=x[1],x_shift=x[2],y_shift=0.082562778,z_shift=x[3],alpha=0,beta=x[4],gamma=0,L1=20.0)
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]


results = minimize(minimisation_func, x0=x0, options={'disp': True})
results = minimize(minimisation_func, x0=x0, bounds=bnds, options={'disp': True})


# bank43/B14
firstIndex=172032
lastIndex=176128

corelli_difc = np.array(mtd['corelli'].extractY().flatten()[firstIndex:lastIndex])
mask = mtd['C60_mask'].extractY().flatten()[firstIndex:lastIndex]
new_difc = mtd['C60_cal'].column('difc')[firstIndex:lastIndex]
new_difc = np.ma.masked_array(new_difc, mask)



x0=[0.88138,0.20955,2.560231046,0.082562778,0.339788726,0,262.44,0,20.0]
results = minimize(minimisation_func, x0=x0, options={'disp': True})

#x,z,a,b,g
x0=[2.560231046,
    0.339788726,
    0,
    262.44,
    0]
bnds = ((x0[0]-0.1,x0[0]+0.1),
        (x0[1]-0.1,x0[1]+0.1),
        (x0[2]-10,x0[2]+10),
        (x0[3]-10,x0[3]+10),
        (x0[4]-10,x0[4]+10))
def minimisation_func(x):
    #difc = get_bank_difc(tube_height=0.88138, bank_width=0.20955,x_shift=0.228238615,y_shift=0.082562778,z_shift=2.572575854,alpha=0,beta=185.07,gamma=0,L1=20.0)
    print x
    difc = get_bank_difc(tube_height=0.88138, bank_width=0.20955,x_shift=x[0],y_shift=0.0965229,z_shift=x[1],alpha=x[2],beta=x[3],gamma=x[4],L1=20.0)
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, bounds=bnds, options={'disp': True})

#height,width,x,z,a,b,g
x0=[0.88138,
    0.20955,
    2.560231046,
    0.339788726,
    0,
    262.44,
    0]
bnds = ((x0[0]-0.1,x0[0]+0.1),
        (x0[1]-0.1,x0[1]+0.1),
        (x0[2]-0.1,x0[2]+0.1),
        (x0[3]-0.1,x0[3]+0.1),
        (x0[4]-10,x0[4]+10),
        (x0[5]-10,x0[5]+10),
        (x0[6]-10,x0[6]+10))
def minimisation_func(x):
    #difc = get_bank_difc(tube_height=0.88138, bank_width=0.20955,x_shift=0.228238615,y_shift=0.082562778,z_shift=2.572575854,alpha=0,beta=185.07,gamma=0,L1=20.0)
    print x
    difc = get_bank_difc(tube_height=x[0], bank_width=x[1],x_shift=x[2],y_shift=0.0965229,z_shift=x[3],alpha=x[4],beta=x[5],gamma=x[6],L1=20.0)
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, bounds=bnds, options={'disp': True})
# results x: array([  9.03236266e-01,   2.09425424e-01,   2.55550148e+00,   3.38729949e-01,   1.65426077e-02,   2.62438211e+02,   -8.33951993e-02])

from matplotlib import pyplot as plt
x=[  9.03236266e-01,   2.09425424e-01,   2.55550148e+00,   3.38729949e-01,   1.65426077e-02,   2.62438211e+02,  -8.33951993e-02]
plt.plot(get_bank_difc(tube_height=x[0], bank_width=x[1],x_shift=x[2],y_shift=0.0965229,z_shift=x[3],alpha=x[4],beta=x[5],gamma=x[6],L1=20.0),label='results')
plt.plot(new_difc,label='cal')
plt.plot(corelli_difc,label='org')
plt.legend()
plt.show()


# bank55/B26
# B26 2584 1.831 20.28 895.178412 82.562778 2422.580236 0 200.28 0
firstIndex=221184
lastIndex=225280

x0=[0.88138,
    0.20955,
    0.895178412,
    2.422580236,
    0,
    200.28,
    0]

#x: array([   0.8912997 ,    0.20650291,    0.88287772,    2.38198232,   2.82540282,  200.49509111,   -0.56109949])


# bank56/B27
# B27 2584 1.831 15.21 677.585904 82.562778 2492.211213 0 195.21 0
firstIndex=225280
lastIndex=229376

x0=[0.88138,
    0.20955,
    0.677585904,
    2.492211213,
    0,
    195.21,
    0]

#x: array([  9.38052598e-01,   2.15495759e-01,   7.00774235e-01,   2.59179858e+00,   6.19189289e+00,   1.97477085e+02,  1.28999464e-01])

# bank55/B26
# B26 2584 1.831 20.28 895.178412 82.562778 2422.580236 0 200.28 0
firstIndex=221184
lastIndex=225280

x0=[0.88138,
    0.20955,
    0.895178412,
    0.082562778,
    2.422580236,
    0,
    200.28,
    0,
    20.0]
bnds = ((x0[0]-0.1,x0[0]+0.1),
        (x0[1]-0.1,x0[1]+0.1),
        (x0[2]-0.1,x0[2]+0.1),
        (x0[3]-0.1,x0[3]+0.1),
        (x0[4]-0.1,x0[4]+0.1),
        (x0[5]-10,x0[5]+10),
        (x0[6]-10,x0[6]+10),
        (x0[7]-10,x0[7]+10),
        (x0[8]-1,x0[8]+1))

#R=[  8.85002483e-01,   2.05150613e-01,   8.82725974e-01,   2.73647207e-02,   2.41341260e+00,   1.03241232e+00,   2.00756862e+02,   3.62333900e+00,   2.03592805e+01]

# bank56/B27
# B27 2584 1.831 15.21 677.585904 82.562778 2492.211213 0 195.21 0
firstIndex=225280
lastIndex=229376

x0=[0.88138,
    0.20955,
    0.677585904,
    0.082562778,
    2.492211213,
    0,
    195.21,
    0,
    20.0]


#R=[  8.78564896e-01,   2.01575686e-01,   6.62672109e-01,   2.54101716e-02,   2.47607766e+00,   4.61583076e+00,   1.95923361e+02,   5.37938698e+00,   2.05353210e+01]



# LaB6
LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_LaB6_19286_19287_sum4.cal', WorkspaceName='LaB6')
MaskBTP(Workspace='LaB6_mask',Pixel="1-16,241-256")
mask = mtd['LaB6_mask'].extractY().flatten()[firstIndex:lastIndex]
new_difc = mtd['LaB6_cal'].column('difc')[firstIndex:lastIndex]
new_difc = np.ma.masked_array(new_difc, mask)

#1 Results
x=[  8.84242215e-01,   2.05442471e-01,   8.82877843e-01,  2.08684700e-02,   2.41373158e+00,   1.79955909e+00,  2.01169730e+02,   4.16977317e+00,   2.04145571e+01]
#2 Results
x=[  8.94730261e-01,   2.06846179e-01,   6.72251116e-01,  6.68520958e-02,   2.47963933e+00,   2.20265792e+00,  1.95571177e+02,   2.20127399e+00,   2.02191801e+01]


plt.plot(get_bank_difc(tube_height=x[0], bank_width=x[1],x_shift=x[2],y_shift=x[3],z_shift=x[4],alpha=x[5],beta=x[6],gamma=x[7],L1=x[8]),label='results')
plt.plot(new_difc,label='cal')
plt.plot(corelli_difc,label='org')
plt.legend()
plt.show()

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
x0=[0.88138,
    0.20955,
    startPos.getX(),
    startPos.getY(),
    startPos.getZ(),
    startRot[1],
    startRot[0],
    startRot[2],
    20.0]
bnds = ((x0[0]-0.1,x0[0]+0.1),
        (x0[1]-0.1,x0[1]+0.1),
        (x0[2]-0.1,x0[2]+0.1),
        (x0[3]-0.1,x0[3]+0.1),
        (x0[4]-0.1,x0[4]+0.1),
        (x0[5]-10,x0[5]+10),
        (x0[6]-10,x0[6]+10),
        (x0[7]-10,x0[7]+10),
        (x0[8]-1,x0[8]+1))


# Refine all                                                                                                                            
def minimisation_func(x):
    print x
    difc = get_bank_difc(tube_height=x[0], bank_width=x[1],x_shift=x[2],y_shift=x[3],z_shift=x[4],alpha=x[5],beta=x[6],gamma=x[7],L1=x[8])
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, options={'disp': True})

print results

# Y Rot only
x0=[0.88138,
    0.20955,
    startPos.getX(),
    startPos.getY(),
    startPos.getZ(),
    startRot[0],
    20.0]
bnds = ((x0[0]-0.1,x0[0]+0.1),
        (x0[1]-0.1,x0[1]+0.1),
        (x0[2]-0.1,x0[2]+0.1),
        (x0[3]-0.1,x0[3]+0.1),
        (x0[4]-0.1,x0[4]+0.1),
        (x0[5]-10,x0[5]+10),
        (x0[6]-1,x0[6]+1))


# Refine all                                                                                                                            
def minimisation_func(x):
    print x
    difc = get_bank_difc(tube_height=x[0], bank_width=x[1],x_shift=x[2],y_shift=x[3],z_shift=x[4],alpha=0,beta=x[5],gamma=0,L1=x[6])
    difc = np.ma.masked_array(difc, mask)
    return chisquare(f_obs=new_difc, f_exp=difc)[0]

results = minimize(minimisation_func, x0=x0, options={'disp': True})

print results
