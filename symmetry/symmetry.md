Symmetry using Mantid
=======
Space-group and symmetry operations in Mantid
-----------
Mantid has a `SpaceGroupFactory` and `SymmetryOperationFactory`, which can be imported by `from mantid.geometry import SymmetryOperationFactory, SpaceGroupFactory`.

You can either get the symmetry operations from a space group or list them all manually.

### Defining a space group
e.g. To get space group 3 (P2):

    sg = SpaceGroupFactory.createSpaceGroup("P 1 1 2")

You can find a complete list of the space groups in Mantid [here](https://github.com/mantidproject/mantid/blob/master/Framework/Geometry/src/Crystal/SpaceGroupFactory.cpp#L454-L995).

Then to get all the symmetry operations from that space group

    symOps = sg.getSymmetryOperations()

### Manually listing symmetries
Alternatively you can list all the symmetry operations individually

    symOps = SymmetryOperationFactory.createSymOps("x,y,z; -y,x-y,z+1/3; -x+y,-x,z; y,x,-z; x-y,-y,-z; -x,-x+y,-z")

### Modifying UB matrix

Get the current UB of the workspace

    ub = ws.sample().getOrientedLattice().getUB()

To calculate the symmetry transformation matrix:
	 
    UBtrans = np.zeros((3,3))
    UBtrans[0] = sym.transformHKL([1,0,0])
    UBtrans[1] = sym.transformHKL([0,1,0])
    UBtrans[2] = sym.transformHKL([0,0,1])
    UBtrans = np.matrix(UBtrans.T)

To calculate the new UB using the tranformation matrix

    new_ub = ub * UBtrans
		
You can then set the UB of a workspace by

    SetUB(ws, UB=ub)

This create a list of UB's that can be looped over.

    ub_list=[]
    for sym in symOps:
        UBtrans = np.zeros((3,3))
        UBtrans[0] = sym.transformHKL([1,0,0])
        UBtrans[1] = sym.transformHKL([0,1,0])
        UBtrans[2] = sym.transformHKL([0,0,1])
        UBtrans = np.matrix(UBtrans.T)
        new_ub = ub*UBtrans
        print "Symmetry transform for "+sym.getIdentifier()
        print UBtrans
        print "New UB:"
        print new_ub
        ub_list.append(new_ub)

Example - Benzil - Space Group 152 (P-3m1)
-------

    ws=CreateSingleValuedWorkspace()
    LoadIsawUB(ws,"/SNS/users/rwp/benzil/benzil_Hexagonal.mat")
    ub=ws.sample().getOrientedLattice().getUB()
    
    sg=SpaceGroupFactory.createSpaceGroup("P 31 2 1")
    symOps = sg.getSymmetryOperations()
    
    for sym in symOps:
    	symTrans = np.array([sym.transformHKL([1,0,0]),
                             sym.transformHKL([0,1,0]),
	                     sym.transformHKL([0,0,1])])
	symTrans=np.matrix(symTrans.T)
	newUB = ub*symTrans
    
    runs=range(29782,29818)
    for r in runs:
	filename='/SNS/CORELLI/IPTS-15526/nexus/CORELLI_'+str(r)+'.nxs.h5'
        print 'Loading run number:'+ str(r)
        data=LoadEventNexus(Filename=filename)
        SetGoniometer(data,Axis0="BL9:Mot:Sample:Axis1,0,1,0,1")
        for ub in ub_list:
            print "using UB:"
            print ub
            SetUB(data, UB=ub)
            md=ConvertToMD(InputWorkspace=data,QDimensions='Q3D',dEAnalysisMode='Elastic', Q3DFrames='HKL',
                           QConversionScales='HKL',MinValues='-10.1,-10.1,-10.1',MaxValues='10.1,10.1,10.1')
            a1,b1=MDNormSCD(InputWorkspace='md',FluxWorkspace='flux',SolidAngleWorkspace='sa',
                            AlignedDim0="[H,H,0],-10.1,10.1,401",
                            AlignedDim1="[H,-H,0],-10.0,10.,401",
                            AlignedDim2="[0,0,L],-5.1,5.1,51")
            if mtd.doesExist('dataMD'):
                dataMD=dataMD+a1
            else:
                dataMD=CloneMDWorkspace(a1)
            if mtd.doesExist('normMD'):
                normMD=normMD+b1
            else:
                normMD=CloneMDWorkspace(b1)
    normData=dataMD/normMD
