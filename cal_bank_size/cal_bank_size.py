#!/usr/bin/env python2
import numpy as np
import math as m

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

for tube in range(16):
    for pixel in range(256):
        p=getPixelPosition(tube,pixel,x_shift=0.228238615,y_shift=0.082562778,z_shift=2.572575854,beta=185.07)
        print tube*256+pixel,calc_difc(p)

from mantid.simpleapi import *
LoadEmptyInstrument(Filename="/SNS/users/rwp/CORELLI_Definition_88.14cm.xml",OutputWorkspace='corelli')
CalculateDIFC(InputWorkspace='corelli',OutputWorkspace='corelli')
corelli_difc = mtd['corelli'].extractY()
corelli_difc[233472:237568] # bank 58

LoadCalFile(InstrumentFilename='/SNS/users/rwp/CORELLI_Definition_88.14cm.xml', CalFilename='/SNS/users/rwp/corelli/cal_2016_02/cal_Si_19284_19285_sum4.cal', WorkspaceName='Si')
new_difc=mtd['Si_cal'].column('difc')
new_difc[233472:237568]
