ws=Load('CNCS_7860')
RemoveLogs(ws)
ws=ConvertUnits(ws,Target='Momentum')
ws=Rebin(ws,'1,1.5,1.5')
ws=CropWorkspace(ws,1.0,1.5)

SA=Rebin(ws,'1,1.5,1.5',PreserveEvents=False)
RemoveWorkspaceHistory(SA)

ws=SumSpectra(ws)
ws=Rebin(ws,'1,1.5,1.5')
el=ws.getSpectrum(0)
el.divide(ws.readY(0)[0],ws.readE(0)[0])

flux=IntegrateFlux(ws, NPoints=10000)
RemoveWorkspaceHistory(flux)

SaveNexus(flux,'flux,nxs')
SaveNexus(SA,'sa.nxs')

SaveNexusProcessed(flux,'flux2.nxs',CompressNexus=True)
SaveNexusProcessed(SA,'sa2.nxs',CompressNexus=True)
