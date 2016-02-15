import matplotlib.pyplot as plt
import numpy as np
import math


x=np.linspace(0, 50000, 5000)
y=np.linspace(0, 8120, 812)
X,Y = np.meshgrid(x,y)


out = np.load('out_373_499.npy')
fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, out)
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('chopper offset (uS)')
fig.savefig('chopper_373_499.png')

fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, out, vmin=0, vmax=math.sqrt(out.max()))
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('chopper offset (uS)')
fig.savefig('chopper_373_499_2.png')


results = np.load('results_373_499.npy')
fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, results, vmin=0)
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('incident flight time (uS)')
fig.savefig('cross_373_499.png')

fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, results, vmin=0, vmax=math.sqrt(results.max()))
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('incident flight time (uS)')
fig.savefig('cross_373_499_2.png')



x=np.linspace(10000, 25000, 1500)
y=np.linspace(0, 8120, 812)
X,Y = np.meshgrid(x,y)


fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, out[:,1000:2500], vmin=0)
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('chopper offset (uS)')
fig.savefig('chopper_373_499_r.png')

fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, out[:,1000:2500], vmin=0, vmax=math.sqrt(out.max()))
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('chopper offset (uS)')
fig.savefig('chopper_373_499_r2.png')



fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, results[:,1000:2500], vmin=0)
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('incident flight time (uS)')
fig.savefig('cross_373_499_r.png')

fig, ax = plt.subplots(figsize=(11,8.5))
p = ax.pcolormesh(X, Y, results[:,1000:2500], vmin=0, vmax=math.sqrt(results.max()))
cb = fig.colorbar(p, ax=ax)
fig.suptitle('DAS_373 pixelID:499*')
ax.set_xlabel('total time of flight (uS)')
ax.set_ylabel('incident flight time (uS)')
fig.savefig('cross_373_499_r2.png')
