import numpy as np

centers=np.loadtxt('centers')

a=(2*25.4+2)/1000
y=np.arange(-7.5*a,8.5*a,a)

for row in centers:
    x = row[3:]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y)[0]
    print(m, c,m*255)
