from mantid.simpleapi import *
from mantid.geometry import SymmetryOperationFactory, SpaceGroupFactory
import numpy as np

#symOps = SymmetryOperationFactory.createSymOps("x,y,z; -y,x-y,z+1/3; -x+y,-x,z+2/3; y,x,-z; x-y,-y,-z+2/3; -x,-x+y,-z+1/3")

ws=CreateSingleValuedWorkspace()
LoadIsawUB(ws,"/SNS/users/rwp/benzil/benzil_Hexagonal.mat")

sg=SpaceGroupFactory.createSpaceGroup("P 1 2 1")
symOps = sg.getSymmetryOperations()


ub=ws.sample().getOrientedLattice().getUB()
print "Starting UB :"
print ub

for sym in symOps:
    symTrans = np.array([sym.transformHKL([1,0,0]),
                         sym.transformHKL([0,1,0]),
                         sym.transformHKL([0,0,1])])
    symTrans=np.matrix(symTrans.T)
    print "Symmetry transform for "+sym.getIdentifier()
    print symTrans
    print "New UB:"
    newUB = ub*symTrans
    print newUB

print "To use SetUB(ws, UB=newUB)"
