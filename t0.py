import numpy as np
import matplotlib.pyplot as plt

e = np.linspace(10,200,100)

t0 = (101.9 * e**(-0.41) * np.exp(-e/282.0))
t0_new = 23.5 * np.exp(-e/205.8)

plt.plot(e, t0)
plt.plot(e, t0_new)
plt.show()
