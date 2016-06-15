LoadEventNexus(Filename='CORELLI_26515',OutputWorkspace='ws')
LoadIsawUB(InputWorkspace='ws',Filename='/SNS/CORELLI/IPTS-16328/shared/FeSe_UB.mat')

ConvertToMD(InputWorkspace='ws', QDimensions='Q3D', dEAnalysisMode='Elastic', QConversionScales='HKL', Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1',OutputWorkspace='hkl', MinValues='-10,-10,-10', MaxValues='10,10,10')
BinMD(InputWorkspace='hkl',AlignedDim0='[H,0,0],-10,2,500', AlignedDim1='[0,K,0],-10,2,500', AlignedDim2='[0,0,L],-5,7,500', OutputWorkspace='hkl2')
SaveMD(InputWorkspace='hkl2',Filename='/SNS/users/rwp/hkl.nxs')
BinMD(InputWorkspace='hkl',AlignedDim0='[H,0,0],-10,2,500', AlignedDim1='[0,0,L],-5,7,500', AlignedDim2='[0,K,0],-10,2,500', OutputWorkspace='hkl_hlk')
SaveMD(InputWorkspace='hkl_hlk',Filename='/SNS/users/rwp/hkl_hlk.nxs')

ConvertToMD(InputWorkspace='ws', QDimensions='Q3D', dEAnalysisMode='Elastic', QConversionScales='HKL', Uproj='1,0,0',Vproj='0,0,1',Wproj='0,1,0',OutputWorkspace='hlk', MinValues='-10,-10,-10', MaxValues='10,10,10')
BinMD(InputWorkspace='hlk',AlignedDim0='[H,0,0],-10,2,500', AlignedDim1='[0,0,L],-5,7,500', AlignedDim2='[0,K,0],-10,2,500', OutputWorkspace='hlk2')
SaveMD(InputWorkspace='hlk2',Filename='/SNS/users/rwp/hlk.nxs')
BinMD(InputWorkspace='hlk',AlignedDim0='[H,0,0],-10,2,500', AlignedDim1='[0,K,0],-10,2,500', AlignedDim2='[0,0,L],-5,7,500', OutputWorkspace='hlk_hkl')
SaveMD(InputWorkspace='hlk2',Filename='/SNS/users/rwp/hlk_hkl.nxs')

ConvertToMD(InputWorkspace='ws', QDimensions='Q3D', dEAnalysisMode='Elastic', QConversionScales='HKL', Uproj='1,1,0',Vproj='0,0,1',Wproj='1,-1,0',OutputWorkspace='hhl', MinValues='-10,-10,-10', MaxValues='10,10,10')
BinMD(InputWorkspace='hhl',AlignedDim0='[H,H,0],-10,10,500', AlignedDim1='[0,0,L],-10,10,500', AlignedDim2='[H,-H,0],-10,10,500', OutputWorkspace='hhl2')
SaveMD(InputWorkspace='hhl2',Filename='/SNS/users/rwp/hhl.nxs')

ConvertToMD(InputWorkspace='ws', QDimensions='Q3D', dEAnalysisMode='Elastic', QConversionScales='HKL', Uproj='1,0.5,0',Vproj='0,0,1',Wproj='1,-1,0',OutputWorkspace='h0.5hl', MinValues='-10,-10,-10', MaxValues='10,10,10')
BinMD(InputWorkspace='h0.5hl',AlignedDim0='[H,0.5H,0],-10,10,500', AlignedDim1='[0,0,L],-10,10,500', AlignedDim2='[H,-H,0],-10,10,500', OutputWorkspace='h0.5hl2')
SaveMD(InputWorkspace='h0.5hl2',Filename='/SNS/users/rwp/hh0.5l.nxs')


# 2D
BinMD(InputWorkspace='hkl', AlignedDim0='[H,0,0],-10,10,500', AlignedDim1='[0,K,0],-10,10,500', OutputWorkspace='hk')
SaveMD(InputWorkspace='hk',Filename='/SNS/users/rwp/hk.nxs')
BinMD(InputWorkspace='hkl', AlignedDim0='[H,0,0],-10,10,500', AlignedDim1='[0,0,L],-10,10,500', OutputWorkspace='hl')
SaveMD(InputWorkspace='hl',Filename='/SNS/users/rwp/hl.nxs')
