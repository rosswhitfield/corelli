outDir = '/SNS/users/rwp/corelli/ZrO2/IPTS-12310/'

LoadEmptyInstrument(InstrumentName='CORELLI', OutputWorkspace='CORELLI')
# Missing banks
MaskBTP('CORELLI', Bank='1-6,14-30,62-72,81-91')
# End of tubes
MaskBTP('CORELLI', Pixel='1-15,242-256')
# Dead tubes
MaskBTP('CORELLI', Bank='45', Tube='16')
MaskBTP('CORELLI', Bank='49', Tube='1')
MaskBTP('CORELLI', Bank='73', Tube='13')
MaskBTP('CORELLI', Bank='80', Tube='6')
# Beam
MaskBTP('CORELLI', Bank='58', Tube='13-16', Pixel='65-145')
MaskBTP('CORELLI', Bank='59', Tube='1-4', Pixel='65-145')

SaveMask('CORELLI', outDir+'mask.xml')

SA, Flux = MDNormSCDPreprocessIncoherent(Filename='CORELLI_8602',
                                         MomentumMin=2.5,
                                         MomentumMax=10,
                                         MaskFile=outDir+'mask.xml')


SaveNexus(SA, outDir+'SA.nxs')
SaveNexus(Flux, outDir+'Flux.nxs')
