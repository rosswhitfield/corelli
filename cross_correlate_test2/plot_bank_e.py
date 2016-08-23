#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(12,6))
total = np.zeros((341,1667))
for bank in range(31,62):
    results = np.zeros((341,1667))
    for run in range(30338,30346):
        filename = 'CORELLI_'+str(run)+'_results_events_bank'+str(bank)+'.npy'
        temp=np.load(filename)
        results += temp
        total += temp
    y,x = results.shape
    xx=np.array(range(x))*10
    yy=np.array(range(y))*10
    X,Y = np.meshgrid(xx,yy)
    plt.clf()
    plt.pcolormesh(X, Y, results, vmin=0, vmax=2000)
    #plt.pcolormesh(X, Y, results)
    plt.colorbar()
    plt.title('bank'+str(bank))
    plt.xlabel('total time of flight (uS)')
    plt.ylabel('incident flight time (uS)')
    plt.savefig('results_events_bank'+str(bank)+'.png')

plt.clf()
plt.pcolormesh(X, Y, total, vmin=0, vmax=50000)
#plt.pcolormesh(X, Y, total)
plt.colorbar()
plt.title('all banks')
plt.xlabel('total time of flight (uS)')
plt.ylabel('incident flight time (uS)')
plt.savefig('results_events_all_bank.png')


L1=20.0
L2=2.585
Lmc=17.999347

Lcs=L1-Lmc
L=L1+L2

chopper_per = 3408.28925864

# +4meV                                                                        
de=-0.004*1.6e-19
m=1.674927351e-27

yyy=xx*Lmc/L
xxx=yyy+yyy*Lcs/Lmc+L2/np.sqrt((Lmc/yyy*1e6)**2+2*de/m)*1e6

plt.clf()
plt.pcolormesh(X, Y, total, vmin=0, vmax=50000)
plt.plot(xx,((xx*Lmc/L)-50)%chopper_per,c='g')
plt.plot(xxx,(yyy-50)%chopper_per,c='r')
plt.colorbar()
plt.title('all banks')
plt.xlabel('total time of flight (uS)')
plt.ylabel('incident flight time (uS)')
plt.savefig('results_events_all_bank_e.png')


plt.clf()
plt.plot(xx,total[0])
plt.plot(xx,total[85])
plt.plot(xx,total[170])
plt.plot(xx,total[255])
plt.show()

#t1=xx*(L1/(L1+L2))
#t2=yy-t1
de=Y.copy()

for ix in range(x):
    for iy in range(y):
        ti = iy*10*1e-6
        vi = Lmc/ti
        Ei = 0.5*m*vi**2
        t1 = L1/vi
        t2 = ix*10*1e-6 - L1/vi
        vf = L2/t2
        Ef = 0.5*m*vf**2
        de = Ef-Ei
        print(ti,vi,Ei,t1,t2,vf,Ef,de)

total_de = np.zeros((200,800))
new_xx = np.zeros((200,800))
de = np.zeros((200,800))
for px in range(800,1600):
    pe = px*10*Lmc/L-50
    for py in range(-100,100):
        ti = (pe + py*10)*1e-6
        vi = Lmc/ti
        Ei = 0.5*m*vi**2
        t1 = L1/vi
        t2 = px*10*1e-6 - L1/vi
        vf = L2/t2
        Ef = 0.5*m*vf**2
        #print(pe,ti,vi,Ei,t1,t2,vf,Ef,(Ef-Ei),(Ef-Ei)/1.602e-19)
        de[py+100,px-800] = Ef-Ei
        new_xx[py+100,px-800]=px*10
        total_de[py+100,px-800] = total[int(((ti*1e6)%chopper_per)/10),px]


de/=1.602e-19

plt.clf()
plt.pcolormesh(new_xx, de, total_de,vmin=0,vmax=20000)
#plt.pcolormesh(new_xx, de, total_de)
plt.colorbar()
plt.ylim(-0.01,0.01)
plt.show()





# 1D define Ei

mev = 15

ei = mev/1e3 * 1.602e-19
vi = np.sqrt(2*ei/m)
ti = Lmc/vi
y = ti*1e6%chopper_per

tof = (L1+L2)/vi
xi = int(tof*1e6/10)

t1 = L1/vi

de_list = []
int_list = []

for ix in range(xi-100,xi+100):
    t2 = xx[ix]/1e6 - t1
    v2 = L2/t2
    ef = 0.5*m*v2**2
    de_list.append((ef-ei)/1.602e-19)
    int_list.append(total[int((y-45)/10),ix])
    #print(ei,vi,ti,tof,ix,t2,v2,ef,ef-ei)

plt.plot(de_list,int_list)
plt.xlim(-0.01,0.01)
plt.title("Ei = "+str(mev)+"meV")
plt.ylabel("Intensity")
plt.xlabel("dE (meV)")
plt.show()
