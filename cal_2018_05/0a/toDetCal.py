import sys
from mantid.kernel import V3D
from mantid.simpleapi import *

workspace_filename = sys.argv[1]

cal=LoadNexus(Filename=workspace_filename)
i=cal.getInstrument()


with open(workspace_filename+'.detcal', 'w') as f:
    f.write('4 DETNUM  NROWS  NCOLS    WIDTH   HEIGHT   DEPTH   DETD   CenterX   CenterY   CenterZ    BaseX    BaseY    BaseZ      UpX      UpY      UpZ\n')

    for bank in range(1,92):
        b=i.getComponentByName("bank"+str(bank)+"/sixteenpack")
        x=b.getPos().getX()*100 # cm
        y=b.getPos().getY()*100 # cm
        z=b.getPos().getZ()*100 # cm
        rot=b.getRotation()
        up = V3D(0,1,0)
        base = V3D(1,0,0)
        rot.rotate(up)
        rot.rotate(base)
        f.write('5 {:6}    256     16  20.0000  78.0000  0.2000  10.00  {: 7.4f} {: 7.4f} {: 7.4f} {: 7.4f} {: 7.4f} {: 7.4f} {: 7.4f} {: 7.4f} {: 7.4f}\n'.format(bank,x,y,z,base.X(),base.Y(),base.Z(),up.X(),up.Y(),up.Z()))
