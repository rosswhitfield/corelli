import sys
from mantid.geometry import SpaceGroupFactory, SymmetryOperationFactory
symOps = sys.argv[1]
symOps = SpaceGroupFactory.subscribedSpaceGroupSymbols(int(symOps))[0]
symOps = SpaceGroupFactory.createSpaceGroup(symOps).getSymmetryOperations()
print("Number of symmetries: {}".format(len(symOps)))
for sym in symOps:
    print(sym.getIdentifier())
