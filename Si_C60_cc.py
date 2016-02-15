c60=Load('CORELLI_2510')
LoadInstrument(c60,InstrumentName='CORELLI')
c60_cc=CorelliCrossCorrelate(c60,TimingOffset=56000)
#c60_cc2=CorelliCrossCorrelate(c60,TimingOffset=63000)

c60q=ConvertUnits(c60,Target="MomentumTransfer",EMode="Elastic")
Rebin(InputWorkspace='c60q', OutputWorkspace='c60q', Params='0.01,0.02,10',PreserveEvents=0)
SumSpectra(InputWorkspace='c60q', OutputWorkspace='c60q')

c60_ccq=ConvertUnits(c60_cc,Target="MomentumTransfer",EMode="Elastic")
Rebin(InputWorkspace='c60_ccq', OutputWorkspace='c60_ccq', Params='0.01,0.02,10',PreserveEvents=0)
SumSpectra(InputWorkspace='c60_ccq', OutputWorkspace='c60_ccq')

c60d=ConvertUnits(c60,Target="dSpacing",EMode="Elastic")
Rebin(InputWorkspace='c60d', OutputWorkspace='c60d', Params='0.01,-0.01,10',PreserveEvents=0)
SumSpectra(InputWorkspace='c60d', OutputWorkspace='c60d')

c60_ccd=ConvertUnits(c60_cc,Target="dSpacing",EMode="Elastic")
Rebin(InputWorkspace='c60_ccd', OutputWorkspace='c60_ccd', Params='0.01,-0.01,10',PreserveEvents=0)
SumSpectra(InputWorkspace='c60_ccd', OutputWorkspace='c60_ccd')


si=Load('/SNS/CORELLI/IPTS-12008/shared/SNS/CORELLI/IPTS-12008/nexus/CORELLI_685')
LoadInstrument(si,InstrumentName='CORELLI')
si_cc=CorelliCrossCorrelate(si,TimingOffset=56000)
#si_cc2=CorelliCrossCorrelate(si,TimingOffset=63000)

siq=ConvertUnits(si,Target="MomentumTransfer",EMode="Elastic")
Rebin(InputWorkspace='siq', OutputWorkspace='siq', Params='0.01,0.02,15')
SumSpectra(InputWorkspace='siq', OutputWorkspace='siq')

si_ccq=ConvertUnits(si_cc,Target="MomentumTransfer",EMode="Elastic")
Rebin(InputWorkspace='si_ccq', OutputWorkspace='si_ccq', Params='0.01,0.02,15')
SumSpectra(InputWorkspace='si_ccq', OutputWorkspace='si_ccq')

sid=ConvertUnits(si,Target="dSpacing",EMode="Elastic")
Rebin(InputWorkspace='sid', OutputWorkspace='sid', Params='0.01,-0.01,5')
SumSpectra(InputWorkspace='sid', OutputWorkspace='sid')

si_ccd=ConvertUnits(si_cc,Target="dSpacing",EMode="Elastic")
Rebin(InputWorkspace='si_ccd', OutputWorkspace='si_ccd', Params='0.01,-0.01,5')
SumSpectra(InputWorkspace='si_ccd', OutputWorkspace='si_ccd')


