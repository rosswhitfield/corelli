outDir = '/SNS/users/rwp/corelli/ZrO2/'

LoadEmptyInstrument(InstrumentName='CORELLI', OutputWorkspace='CORELLI')
# Missing banks
MaskBTP('CORELLI', Bank='1-9,14-30,62-71,75-91')
# End of tubes
MaskBTP('CORELLI', Pixel='1-15,242-256')
# Beam
MaskBTP('CORELLI', Bank='58', Tube='13-16', Pixel='65-145')
MaskBTP('CORELLI', Bank='59', Tube='1-4', Pixel='65-145')

SaveMask('CORELLI', outDir+'mask_2432.xml')

SA, Flux = MDNormSCDPreprocessIncoherent(Filename='CORELLI_2432',
                                         MomentumMin=2.5,
                                         MomentumMax=10,
                                         MaskFile=outDir+'mask_2432.xml')


SaveNexus(SA, outDir+'SA_2432.nxs')
SaveNexus(Flux, outDir+'Flux_2432.nxs')
