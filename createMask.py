from mantid.simpleapi import LoadEmptyInstrument, MaskBTP, SaveMask

LoadEmptyInstrument(InstrumentName='CORELLI', OutputWorkspace='CORELLI')

# Missing banks
MaskBTP('CORELLI', Bank='1-6,29,30,62,63-68,91')

# End of tubes
MaskBTP('CORELLI', Pixel='1-15,242-256')

# Beam center
MaskBTP('CORELLI', Bank='58', Tube='13-16', Pixel='80-130')
MaskBTP('CORELLI', Bank='59', Tube='1-4', Pixel='80-130')

SaveMask('CORELLI', 'corelli_mask.xml')

