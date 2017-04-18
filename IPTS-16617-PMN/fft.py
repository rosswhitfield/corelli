LoadMD(Filename='/SNS/users/rwp/corelli/IPTS-16617-PMN/PMN_normdata_48sym_300K.nxs', LoadHistory=False, OutputWorkspace='pmn')

q_max=10
q_max=6.5
q_max=4.8
q_max=1.8

DeltaPDF3D(InputWorkspace='pmn',  OutputWorkspace='fft', CropSphere=True, SphereMin='0.2', SphereMax=q_max)
SaveMD('fft','/SNS/users/rwp/corelli/IPTS-16617-PMN/PMN_normdata_48sym_300K_fft_q_max'+str(q_max)+'.nxs')
