import matplotlib.pyplot as plt
import numpy as np
from nexusformat import nexus as nx

a=nx.nxload("/SNS/CORELLI/IPTS-15526/shared/benzil_100K_normData_sym_All_noCC.nxs")

x = np.linspace(-10, 10, 401)
y = np.linspace(-17.5, 17.5, 401)
X, Y = np.meshgrid(x, y)
plt.pcolormesh(x,y,a)
