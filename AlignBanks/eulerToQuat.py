import math
_deg2rad = math.pi/180.0

def eulerToQuat(a,b,c,convention="YZX"):
    if len(convention)!=3:
        print "Error with convention, must be length 3"
        return
    if convention[0]==convention[1] or convention[1]==convention[2]:
        print "Error with convention, can't repeat character"
        return
    if convention[0] not in ['X','Y','Z'] or convention[1] not in ['X','Y','Z'] or convention[2] not in ['X','Y','Z']:
        print "Error with convention, must be X, Y or Z."
        return
    quat=[0,0,0,0]
    for a in convention:
        

def quatFromAngle(w,a):
    q0=math.cos(0.5*w*_deg2rad)
    qx=math.sin(0.5*w*_deg2rad)
    if a == 'X':
        return (q0,qx,0,0)
    elif a =='Y':
        return (q0,0,qx,0)
    elif a =='Z':
        return (q0,0,0,qx)
    else:
        print "nope"
        return

def normQuat(w,a,b,c):
