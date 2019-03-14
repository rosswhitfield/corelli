import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import h5py
import numpy as np

IPTS = 21655
runs = range(91699,91771)

count_dict = {}
for bank in range(1,92):
    count_dict[bank] = []

mon_dict = {}
for mon in range(1,3):
    mon_dict[mon] = []

total = []

for run in runs:
    filename = '/SNS/CORELLI/IPTS-{}/nexus/CORELLI_{}.nxs.h5'.format(IPTS,run)
    print(run)
    with h5py.File(filename,'r') as f:
        for bank in range(1,92):
            count_dict[bank].append(f['entry/bank{}_events/total_counts'.format(bank)].value[0])
        for mon in range(1,3):
            mon_dict[mon].append(f['entry/monitor{}/total_counts'.format(mon)].value[0])
        total.append(f['entry/total_counts'].value[0])

for bank in range(1,92):
    fig,ax=plt.subplots()
    ax.plot(np.linspace(0,355,len(runs)),count_dict[bank])
    fig.savefig('bank{}.png'.format(bank))

for mon in range(1,3):
    fig,ax=plt.subplots()
    ax.plot(np.linspace(0,355,len(runs)),mon_dict[mon])
    fig.savefig('monitor{}.png'.format(mon))

fig,ax=plt.subplots()
ax.plot(np.linspace(0,355,len(runs)),total)
fig.savefig('total.png')
