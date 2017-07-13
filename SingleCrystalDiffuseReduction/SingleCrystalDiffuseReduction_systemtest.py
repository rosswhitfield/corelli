from mantid.simpleapi import *

CORELLI_29782=Load("/SNS/CORELLI/IPTS-15526/nexus/CORELLI_29782.nxs.h5")
SaveNexus(CORELLI_29782,"CORELLI_29782.nxs")
CORELLI_29792=Load("/SNS/CORELLI/IPTS-15526/nexus/CORELLI_29792.nxs.h5")
SaveNexus(CORELLI_29792,"CORELLI_29792.nxs")


SingleCrystalDiffuseReduction(Filename='CORELLI_29782,CORELLI_29792',
                              SolidAngle='SingleCrystalDiffuseReduction_SA.nxs',
                              Flux='SingleCrystalDiffuseReduction_Flux.nxs',
                              UBMatrix="SingleCrystalDiffuseReduction_UB.mat",
                              OutputWorkspace='SCDR_output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-7.5375,7.5375,201',
                              BinningDim1='-13.165625,13.165625,201',
                              BinningDim2='-0.1,0.1,1',
                              SymmetryOps="P 31 2 1")

