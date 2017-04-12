from mantid.simpleapi import LoadMD
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

benzil = LoadMD('/SNS/users/rwp/benzil/300K_fft.nxs')
signal = benzil.getSignalArray()
x, y = np.meshgrid(np.linspace(-10,10,501),np.linspace(-10,10,501))
plt.pcolormesh(x, y, signal[:,:,260], norm=colors.SymLogNorm(linthresh=0.1, linscale=0, vmin=-1.0, vmax=1.0), cmap='RdBu_r')
plt.colorbar()
plt.show()
