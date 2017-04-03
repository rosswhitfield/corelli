#!/usr/bin/python2
from __future__ import print_function
from mantid.simpleapi import LoadEmptyInstrument, MoveInstrumentComponent, mtd

LoadEmptyInstrument(Filename='/SNS/users/rwp/CORELLI_Definition_91.07cm.xml', OutputWorkspace='ws')
ws= mtd['ws']
#[x,_,z] = mtd['ws'].getInstrument().getComponentByName('CORELLI/bank46/sixteenpack/tube3/pixel128').getPos()
#[_,y,_] = mtd['ws'].getInstrument().getComponentByName('CORELLI/bank46/sixteenpack/tube3').getPos()
#MoveInstrumentComponent('ws', ComponentName='CORELLI/bank46/sixteenpack/tube3/pixel128', X=x, Y=y, Z=z, RelativePosition=False)

def pixel(A, E1, E2, x):
    return 255*A*(x-E1)/(E2-E1+(A-1)*(x-E1))

with open('curvefitmain.txt', "r") as f:
    lines = f.readlines()

lengths=[]
for line in lines:
    if not 'channel' in line:
        continue
    _, channel, _, roc, _, A, _, E1, _, E2 = line.split()
    channel = float(channel)
    roc = float(roc)
    A = float(A)
    E1 = float(E1)
    E2 = float(E2)
    lengths.append(E2-E1)
    print(roc,channel,A,E1,E2)
    print(pixel(A, E1, E2, 85))
    print(pixel(A, E1, E2, 432))
    print(pixel(A, E1, E2, 785))
