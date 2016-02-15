from mantid.kernel import Quat, V3D
import math

def eulerToQuat(a,b,c,convention="YZX"):
    getV3D={'X':V3D(1,0,0),'Y':V3D(0,1,0),'Z':V3D(0,0,1)}
    q1=Quat(a,getV3D[convention[0]])
    q2=Quat(b,getV3D[convention[1]])
    q3=Quat(c,getV3D[convention[2]])
    return q1*q2*q3

def eulerToAngleAxis(a,b,c,convention="YZX"):
    getV3D={'X':V3D(1,0,0),'Y':V3D(0,1,0),'Z':V3D(0,0,1)}
    q1=Quat(a,getV3D[convention[0]])
    q2=Quat(b,getV3D[convention[1]])
    q3=Quat(c,getV3D[convention[2]])
    q=q1*q2*q3
    # Semi-angle in radians
    deg = math.acos(q[0])
    # Prefactor for the axis part
    s = math.sin(deg)
    # Angle in degrees
    deg *= 360.0 / math.pi
    ax0 = q[1] / s
    ax1 = q[2] / s
    ax2 = q[3] / s
    return deg,ax0,ax1,ax2
