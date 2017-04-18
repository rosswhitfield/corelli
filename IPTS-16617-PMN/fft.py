LoadMD(Filename='/SNS/users/rwp/corelli/IPTS-16617-PMN/PMN_normdata_48sym_300K.nxs', LoadHistory=False, OutputWorkspace='pmn')


DeltaPDF3D(InputWorkspace='pmn', IntermediateWorkspace='i_10', OutputWorkspace='fft_10', CropSphere=True, SphereMin='0.2', SphereMax='10')
DeltaPDF3D(InputWorkspace='pmn', IntermediateWorkspace='i_6.5', OutputWorkspace='fft_6.5', CropSphere=True, SphereMin='0.2', SphereMax='6.5')
DeltaPDF3D(InputWorkspace='pmn', IntermediateWorkspace='i_6.5', OutputWorkspace='fft_4.8', CropSphere=True, SphereMin='0.2', SphereMax='4.8')
DeltaPDF3D(InputWorkspace='pmn', IntermediateWorkspace='i_1.8', OutputWorkspace='fft_1.8', CropSphere=True, SphereMin='0.2', SphereMax='1.2')
