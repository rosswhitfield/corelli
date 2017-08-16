import sys
sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *


vanadium = r'/SNS/TOPAZ/IPTS-15376/shared/calibration/TOPAZ_15670_event.nxs'
nosample = r'/SNS/TOPAZ/IPTS-15376/shared/calibration/TOPAZ_15671_event.nxs'
geometryfile=r'/SNS/TOPAZ/IPTS-15376/shared/calibration/TOPAZ_2016A.DetCal'
groupingfile=r'/SNS/TOPAZ/IPTS-15376/shared/calibration/TOPAZ_grouping_2016A.xml'

calibrationdir ='/SNS/users/3y9/Desktop/MDTutorial/tmp/'

#load background, and get the proton charge
BKG=Load(Filename=nosample)
LoadIsawDetCal(InputWorkspace=BKG, Filename=geometryfile)
BKGPC=BKG.getRun().getProtonCharge()

#load vanadium, and substract scated background
rawVan=Load(Filename=vanadium)
LoadIsawDetCal(InputWorkspace=rawVan, Filename=geometryfile)
rawVanPC=rawVan.getRun().getProtonCharge()
temp=BKG*(rawVanPC/BKGPC)
rawVan=Minus(LHSWorkspace=rawVan, RHSWorkspace=temp)

#Absorption correction and masking
rawVan=CropWorkspace(InputWorkspace=rawVan,XMin='500.0',XMax='16000.0')
rawVan=AnvredCorrection(InputWorkspace=rawVan,
                        LinearScatteringCoef='0.367',LinearAbsorptionCoef='0.366',
                        Radius='0.20',OnlySphericalAbsorption='1',PowerLambda ='0')
rawVan=ConvertUnits(InputWorkspace=rawVan,Target='Momentum')
MaskBTP(Workspace=rawVan,Bank="10-12,15,21,24-25,30-32,35,40-45,50-59")
MaskBTP(Workspace=rawVan,Pixel="0-20,235-255")
MaskBTP(Workspace=rawVan,Tube="0-20,235-255")

#Change the Xmin and Xmax in units of Momentum 2pi/lambda
rawVan=CropWorkspace(InputWorkspace=rawVan,XMin='1.8',XMax='12.5')

#The sa is a spatial sensitivity correction
sa=Rebin(InputWorkspace=rawVan,Params='1.80,12.5,12.5',PreserveEvents='0')
SaveNexus(InputWorkspace=sa, Filename=calibrationdir+"solidAngle.nxs")

#Check grouping file. Need to match the current instrument config.
#The flux has the event data corrected for absorption
flux=Rebin(InputWorkspace=rawVan,Params='1.80,12.5,12.5',PreserveEvents='1')
flux=GroupDetectors(InputWorkspace=flux,MapFile=groupingfile)
#DeleteWorkspace(rawVan)
#DeleteWorkspace(BKG)
AnalysisDataService.remove( rawVan.getName() )
#AnalysisDataService.remove( BKG.getName() )

flux=CompressEvents(InputWorkspace=flux,Tolerance=1e-4)
flux=Rebin(InputWorkspace=flux,Params='1.50,12.5,12.5')
#Normalize each flux spectrum to one
#readY(i) get the histogram representation of the spectrum
#readY(i)[0] is the total number of events in the spectrum sine there is only one bin
for i in range(flux.getNumberHistograms()):
    el=flux.getEventList(i)
    if flux.readY(i)[0] > 0:
        # No error estimates
        #el.divide(flux.readY(i)[0],0)
        el.divide(flux.readY(i)[0],flux.readE(i)[0])
SortEvents(InputWorkspace=flux, SortBy="X Value")
flux=IntegrateFlux(flux,NPoints=10000)
SaveNexus(InputWorkspace=flux, Filename=calibrationdir+"spectra.nxs")



