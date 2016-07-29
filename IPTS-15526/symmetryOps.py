import numpy as np
from mantid.geometry import SymmetryOperationFactory

symOps = SymmetryOperationFactory.createSymOps("x,y,z; -y,x-y,z+1/3; -x+y,-x,z+2/3; y,x,-z; x-y,-y,-z+2/3; -x,-x+y,-z+1/3")
ub = np.eye(3)
new = np.eye(3)
for sym in symOps:
    for row in range(3):
        new[row] = sym.transformHKL(ub[row])
    new=new.T
    print "Symmetry transform for "+sym.getIdentifier()
    print new
