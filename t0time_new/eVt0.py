from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import numpy as np

# sed 's/%_[0-9]* *[A-Za-z]*.//' CORELLI_14161_m3.peaks | sort -n | column -t > CORELLI_14161_m3_clean.peaks
# fit gaussian with fityk

def calc_e_t0(m2_peaks,m3_peaks):
    NeutronMass = 1.674927211e-27
    meV = 1.602176487e-22
    d=6.502
    distanceMtoM3=24.554
    distanceMtoM2=18.052
    e=[]
    t0=[]
    for i in range(len(m2_peaks)):
        v=d/(m3_peaks[i]-m2_peaks[i])
        e.append(v**2*0.5e+12*NeutronMass/meV)
        t0.append(m2_peaks[i]-distanceMtoM2/v)
        #print i,m2_peaks[i],m2_peaks[i],v,e[i],t0[i]
    return e,t0

m2_peaks=np.loadtxt("CORELLI_14161_m2_clean.peaks")[:,0]
m3_peaks=np.loadtxt("CORELLI_14161_m3_clean.peaks")[:,0]
[e_14161,t0_14161]=calc_e_t0(m2_peaks,m3_peaks)
plt.plot(e_14161,t0_14161,'o',label="14161 120Hz")

m2_peaks=np.loadtxt("CORELLI_13116_m2_clean.peaks")[:,0]
m3_peaks=np.loadtxt("CORELLI_13116_m3_clean.peaks")[:,0]
[e_13116,t0_13116]=calc_e_t0(m2_peaks,m3_peaks)
plt.plot(e_13116,t0_13116,'o',label="13116 60Hz")

m2_peaks=np.loadtxt("CORELLI_14329_m2_clean.peaks")[:,0]
m3_peaks=np.loadtxt("CORELLI_14329_m3_clean.peaks")[:,0]
[e_14329,t0_14329]=calc_e_t0(m2_peaks,m3_peaks)
plt.plot(e_14329,t0_14329,'o',label="14329 120Hz")

m2_peaks=np.loadtxt("CORELLI_14061-4_m2_clean.peaks")[:,0]
m3_peaks=np.loadtxt("CORELLI_14061-4_m3_clean.peaks")[:,0]
[e_14061,t0_14061]=calc_e_t0(m2_peaks,m3_peaks)
plt.plot(e_14061,t0_14061,'o',label="14061-4 180Hz")


plt.legend()
plt.show()

np.savetxt("CORELLI_14161_t0_e.txt",np.transpose(np.array([e_14161,t0_14161])))
np.savetxt("CORELLI_13116_t0_e.txt",np.transpose(np.array([e_13116,t0_13116])))
np.savetxt("CORELLI_14329_t0_e.txt",np.transpose(np.array([e_14329,t0_14329])))
np.savetxt("CORELLI_14061-4_t0_e.txt",np.transpose(np.array([e_14061,t0_14061])))



plt.plot(e_14161[2:-4],t0_14161[2:-4],'o',label="14161 120Hz")
plt.plot(e_13116,t0_13116,'o',label="13116 60Hz")
plt.plot(e_14329[14:],t0_14329[14:],'o',label="14329 120Hz")
plt.plot(e_14061[:-9],t0_14061[:-9],'o',label="14061-4 180Hz")
plt.legend()
plt.show()

e=e_14161[2:-4]+e_13116+e_14329[14:]+e_14061[:-9]
t0=t0_14161[2:-4]+t0_13116+t0_14329[14:]+t0_14061[:-9]


def t_zero(x,A,B,C):
    return A*x**(-B)*np.exp(x/-C)

def t_zero(x,A,B):
    return A*np.exp(x/-B)

popt, pcov = curve_fit(t_zero,e,t0)
ex=np.array(range(5,500))
A=101.9
B=0.41
C=282.0
plt.plot(ex,A*ex**(-B)*np.exp(-ex/C))
plt.plot(e,t0,'o',markersize=5)
plt.plot(ex,t_zero(ex,popt[0],popt[1]))
plt.show()
    
plt.plot(ex,t_zero(ex,popt[0],popt[1]))
plt.plot(ex,t_zero(ex,23.5,205.8))
plt.show()
