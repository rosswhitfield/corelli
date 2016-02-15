from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


filename="CORELLI_11005" #120Hz
filename="CORELLI_11004" #60Hz

resolution=1
scale=18/(18+0.052)

LoadNexusMonitors(Filename='/SNS/CORELLI/IPTS-12310/nexus/'+filename+'.nxs.h5',OutputWorkspace=filename)
LoadInstrument(Workspace=filename,Filename='/SNS/users/rwp/CORELLI_Definition.xml')
#ScaleX(InputWorkspace=filename+'_monitors',OutputWorkspace=filename+'_monitors',Factor=str(scale))
Rebin(InputWorkspace=filename,OutputWorkspace=filename,Params='0,'+str(resolution)+',16667')

w = mtd[filename]
sequence = map(float,w.getInstrument().getComponentByName('correlation-chopper').getStringParameter('sequence')[0].split())
freq = round(w.getRun().getProperty("BL9:Chop:Skf4:MotorSpeed").timeAverageValue())
delay = w.getRun().getProperty("BL9:Chop:Skf4:PhaseTimeDelaySet").timeAverageValue()

print filename,'MotorSpeed =',freq,'Hz','PhaseTimeDelaySet =',delay,'uS'


source = w.getInstrument().getSource()
cc = w.getInstrument().getComponentByName("correlation-chopper")
print source.getDistance(cc)
print source.getDistance(w.getInstrument().getComponentByName("monitor2"))
distanceMtoM3 = source.getDistance(w.getInstrument().getComponentByName("monitor3"))
distanceMtoM2 = source.getDistance(w.getInstrument().getComponentByName("monitor2"))

distanceM2toM3 = w.getInstrument().getComponentByName("monitor2").getDistance(w.getInstrument().getComponentByName("monitor3"))

scale_m2 = source.getDistance(w.getInstrument().getComponentByName("monitor2"))/source.getDistance(cc)
scale_m3 = source.getDistance(w.getInstrument().getComponentByName("monitor3"))/source.getDistance(cc)

sequence2=sequence
for i in range(int(freq/60)-1):
    sequence2 = np.append(sequence2,sequence)

x=w.extractX()[1]
y=w.extractY()[1]
x2=w.extractX()[2]
y2=w.extractY()[2]




s=np.cumsum(sequence2)
chopper=np.zeros(len(x)-1)
chopper_n=np.zeros(len(x)-1)
l=len(chopper)

for n in range(l):
    i=np.searchsorted(s*scale_m2,((x[n]+x[n+1]) / 2 / 16666.67)*360.*freq/60.)
    chopper_n[n]=i
    if i%2==1:
        chopper[n]=1

chopper2=np.zeros(len(chopper)*2)
chopper2=np.append(chopper,chopper)

corr=np.correlate(y,chopper2)
r=np.argmax(corr)
r2=(x[r]+x[r+1]) / 2

print "Chopper sequence offset = ",r2,"uS"


s=np.cumsum(sequence2)
m3chopper=np.zeros(len(x)-1)
m3chopper_n=np.zeros(len(x)-1)
l=len(m3chopper)

for n in range(l):
    i=np.searchsorted(s*scale_m3,((x[n]+x[n+1]) / 2 / 16666.67)*360.*freq/60.)
    m3chopper_n[n]=i
    if i%2==1:
        m3chopper[n]=1

m3chopper2=np.zeros(len(m3chopper)*2)
m3chopper2=np.append(m3chopper,m3chopper)

corr=np.correlate(y2,m3chopper2)
m3r=np.argmax(corr)
m3r2=(x[m3r]+x[m3r+1]) / 2

print "Chopper sequence offset = ",m3r2,"uS"




#chopper=np.roll(chopper,r)
#m3chopper=np.roll(m3chopper,m3r)
#plt.plot(x[:-1],y)
#plt.plot(x[:-1],y2)
#plt.plot(x[:-1],chopper*y.max()*0.5)
#plt.plot(x[:-1],m3chopper*y2.max()*0.5)
#plt.show()


NeutronMass = 1.674927211e-27
meV = 1.602176487e-22



cn=np.roll(chopper_n,r)
m3cn=np.roll(m3chopper_n,m3r)

def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2*sigma**2))

def gauss_plot(x, p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2*sigma**2))



def step(x,A,mu,sigma):
    if np.abs(x-mu)>sigma:
        return 0
    else:
        return A

#def gauss(x, *p):
#    A,mu,sigma = p
    #print 'x = ',x
    #print 'p = ',p
#    return [step(xi,A,mu,sigma) for xi in x]

#def gauss_plot(x, p):
#    return [step(xi,A,mu,sigma) for xi in x]


def trap(x,A,mu,sigma1,sigma2):
    if np.abs(x-mu)>sigma1:
        return 0
    elif np.abs(x-mu)>sigma2:
        return A*(sigma1-abs(x-mu))/(sigma1-sigma2)
    else:
        return A

#def gauss(x, *p):
#    A,mu,sigma1,sigma2 = p
#    return [trap(xi,A,mu,sigma1,sigma2) for xi in x]

#def gauss_plot(x, p):
#    return [trap(xi,p[0],p[1],p[2],p[3]) for xi in x]




coeff2=np.array([0,0,0])
coeff3=np.array([0,0,0])
results_2=[]
results_3=[]
results_v=[]
results_e=[]
results_t0=[]
for n in range(1,87,2):
    m2w=np.where(cn==n)
    extra=48
    start=m2w[0][0]-extra
    end=m2w[0][-1]+extra
    fit_x=x[start:end]
    fit_y=y[start:end]
    m3w=np.where(m3cn==n)
    m3start=m3w[0][0]-extra
    m3end=m3w[0][-1]+extra
    m3fit_x=x2[m3start:m3end]
    m3fit_y=y2[m3start:m3end]
    if fit_x[0]<3000 or fit_x[-1]>12250 or m3fit_x[0]<4000 or m3fit_x[-1]>16666:
        continue
    #plt.plot(fit_x,fit_y)
    #plt.plot(m3fit_x,m3fit_y)
    #plt.show()
    p0=[fit_y.max(),fit_x[len(fit_x)/2],len(fit_x)/4.]
    p0=[fit_y.max(),fit_x[len(fit_x)/2],len(fit_x)/3.,len(fit_x)/4.]
    try:
        coeff2, var_matrix = curve_fit(gauss,fit_x,fit_y,p0=p0)
    except:
        coeff2[1]=0.
    p0=[m3fit_y.max(),m3fit_x[len(m3fit_x)/2],len(m3fit_x)/4.]
    p0=[m3fit_y.max(),m3fit_x[len(m3fit_x)/2],len(m3fit_x)/3.,len(m3fit_x)/4.]
    try:
        coeff3, var_matrix = curve_fit(gauss,m3fit_x,m3fit_y,p0=p0)
    except:
        coeff3[1]=0.
    if (len(coeff2.nonzero()[0])==4 and len(coeff3.nonzero()[0])==4):
        results_2.append(coeff2)
        results_3.append(coeff3)
        v = distanceM2toM3/(coeff3[1]-coeff2[1])
        t0 = coeff3[1]-distanceMtoM3/v
        #t0 = coeff2[1]-distanceMtoM2/v
        e = v**2*0.5e+12*NeutronMass/meV
        results_v.append(v)
        results_e.append(e)
        results_t0.append(t0)
        print n,coeff2,coeff3,v,e,t0
        plt.scatter(fit_x,fit_y,label='BM2')
        plt.plot(fit_x,gauss_plot(fit_x,coeff2),label='BM2 fit')
        plt.scatter(m3fit_x,m3fit_y,label='BM3')
        plt.plot(m3fit_x,gauss_plot(m3fit_x,coeff3),label='BM3 fit')
        plt.legend()
        plt.show()



x_arcs=np.arange(10,200)
def arcs(dummy):
    return 101.9*dummy**(-0.41)*np.exp(dummy/-282.0)

plt.plot(x_arcs,arcs(x_arcs))
plt.scatter(results_e,results_t0)
plt.show()



plt.plot(chopper_n,label='chopper_n')
plt.plot(cn,label='cn')
plt.plot(m3chopper_n,label='m3chopper_n')
plt.plot(m3cn,label='m3cn')
plt.legend()
plt.show()
