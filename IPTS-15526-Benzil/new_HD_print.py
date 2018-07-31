from mantid.simpleapi import *

sa='/SNS/CORELLI/shared/Vanadium/2016B/SolidAngle20160720NoCC.nxs'
flux='/SNS/CORELLI/shared/Vanadium/2016B/Spectrum20160720NoCC.nxs'

SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle=sa,
                              Flux=flux,
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-10.0125,10.0125,801',
                              BinningDim1='-17.521875,17.521875,801',
                              BinningDim2='-0.1,1.1,6',
                              SymmetryOps="P 31 2 1")
SaveMD('output', Filename='/SNS/users/rwp/benzil/benzil_300K_volume_801_801.nxs')



SingleCrystalDiffuseReduction(Filename='CORELLI_29782:29817',
                              Background='CORELLI_28124',
                              BackgroundScale=0.95,
                              SolidAngle=sa,
                              Flux=flux,
                              UBMatrix="/SNS/CORELLI/IPTS-15526/shared/benzil_Hexagonal.mat",
                              OutputWorkspace='output',
                              SetGoniometer=True,
                              Axis0="BL9:Mot:Sample:Axis1,0,1,0,1",
                              Uproj='1,1,0',
                              Vproj='1,-1,0',
                              Wproj='0,0,1',
                              BinningDim0='-6.255,6.255,1251',
                              BinningDim1='-10.849991275878653,10.849991275878653,1251',
                              BinningDim2='-0.1,1.1,6',
                              SymmetryOps="P 31 2 1")
SaveMD('output', Filename='/SNS/users/rwp/benzil/benzil_300K_volume_1251_1251.nxs')
