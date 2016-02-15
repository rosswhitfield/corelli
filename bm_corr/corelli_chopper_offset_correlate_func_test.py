import matplotlib.pyplot as plt
from corelli_chopper_offset_correlate_func import *


calc_offset("CORELLI_317",plot=True)
calc_offset("CORELLI_325",plot=True)
calc_offset("CORELLI_329",plot=True)
calc_offset("CORELLI_331",plot=True)

calc_offset("CORELLI_317",scale=18/(18+0.05),plot=True)
calc_offset("CORELLI_325",scale=18/(18+0.05),plot=True)
calc_offset("CORELLI_329",scale=18/(18+0.05),plot=True)
calc_offset("CORELLI_331",scale=18/(18+0.055),plot=True)


calc_offset_plot("CORELLI_317",scale=18/(18+0.055))
calc_offset_plot_norm("CORELLI_317",scale=18/(18+0.055))
calc_offset_plot_norm("CORELLI_325",scale=18/(18+0.055))
calc_offset_plot_norm("CORELLI_329",scale=18/(18+0.055))
calc_offset_plot_norm("CORELLI_331",scale=18/(18+0.055))



corr=[0]*20
x=[0]*20
for n in range(0,20):
    (a,b,c,d)=calc_offset("CORELLI_331",1,scale=18./(18.+n/200.))
    corr[n]=d
    x[n]=n/200.

plt.plot(x,corr)
plt.show()


corr=np.zeros([2,100])
for n in range(0,100):
    (a,b,c,d)=calc_offset("CORELLI_331",1,scale=18./(18.+n/1000.))
    corr[1,n]=d
    corr[0,n]=n/1000.

np.save("/SNS/users/rwp/CORELLI_331_corr",corr)
plt.plot(corr[0,:],corr[1,:])
plt.show()



l=len(range(317,333))
a=[0]*l
b=[0]*l
c=[0]*l
d=[0]*l
for n in range(317,333):
    i=n-317
    filename='CORELLI_'+str(n)
    (a[i],b[i],c[i],d[i])=calc_offset(filename,1,scale=18./(18.+0.055))
    i=+1

for n in range(317,333):
    i=n-317
    filename='CORELLI_'+str(n)
    print filename,'MotorSpeed =',a[i],'Hz','PhaseTimeDelaySet =',b[i],'uS','CalculatedOffset =',c[i],'uS'

