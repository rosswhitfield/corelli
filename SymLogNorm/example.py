from mantid.simpleapi import LoadMD
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.transforms as mtransforms
import numpy as np

benzil = LoadMD('/SNS/users/rwp/benzil/benzil_300K_bkg_subtract_sym_All_noCC_flat2_fft.nxs')
signal = benzil.getSignalArray()


x, y = np.meshgrid(np.linspace(-10,10,501),np.linspace(-10,10,501))
plt.pcolormesh(x, y, signal[:,:,252], norm=colors.SymLogNorm(linthresh=0.2, linscale=0, vmin=-1.0, vmax=1.0), cmap='coolwarm')
plt.colorbar()
plt.show()

plt.pcolormesh(x, y, signal[:,260,:], norm=colors.SymLogNorm(linthresh=0.05, linscale=1, vmin=-1.0, vmax=1.0), cmap='coolwarm')
plt.colorbar()
plt.show()


fig = plt.pcolormesh(x, y, signal[:,:,252].transpose(), vmax=1,vmin=0,cmap='viridis')
trans_data = mtransforms.Affine2D().skew(np.arctan(np.sin(np.deg2rad(-30))), 0) + fig.get_transform()
fig.set_transform(trans_data)
plt.show()


fig = plt.pcolormesh(x, y, signal[:,:,252], norm=colors.SymLogNorm(linthresh=0.1, linscale=1, vmin=-1.0, vmax=1.0), cmap='coolwarm')
trans_data = mtransforms.Affine2D().skew(np.arctan(np.sin(np.deg2rad(-30))), 0) + fig.get_transform()
fig.set_transform(trans_data)
plt.colorbar()
plt.show()
