import sys
sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
from math import sqrt
import numpy as np

def getPeakIntensity(F,  SqError,  minIntensity,  noPoints):
    measuredPoints  = 0
    peakPoints  = 0
    peakSum = 0.0
    measuredSum = 0.0
    errSqSum = 0.0
    measuredErrSqSum = 0.0
    Peak = np.zeros((F.shape))
    PeakErr2 = np.zeros((F.shape))
    for Hindex in range(F.shape[0]):
        for Kindex in range(F.shape[1]):
            for Lindex in range(F.shape[2]):
                if not np.isnan(F[Hindex,  Kindex,  Lindex]) and not np.isinf(F[Hindex,  Kindex,  Lindex]):
                    measuredPoints = measuredPoints + 1
                    measuredSum = measuredSum + F[Hindex,  Kindex,  Lindex] 
                    measuredErrSqSum = measuredErrSqSum + SqError[Hindex,  Kindex,  Lindex]
                    if F[Hindex,  Kindex,  Lindex] > minIntensity:
                        neighborPoints  = 0
                        for Hj in range(-2,  3):
                            for Kj in range(-2,  3):
                                for Lj in range(-2,  3):
                                    if Lindex+Lj >=   0 and Lindex+Lj < F.shape[2]  and Kindex+Kj >=   0 and Kindex+Kj < F.shape[1] and Hindex+Hj >=   0 and Hindex+Hj < F.shape[0] and F[Hindex+Hj,  Kindex+Kj,  Lindex+Lj] > minIntensity:
                                        neighborPoints = neighborPoints + 1
                        if neighborPoints >=  noPoints:
                            Peak[Hindex,  Kindex,  Lindex] = F[Hindex,  Kindex,  Lindex]
                            PeakErr2[Hindex,  Kindex,  Lindex] = SqError[Hindex,  Kindex,  Lindex]
                            peakPoints = peakPoints + 1
                            peakSum = peakSum + F[Hindex,  Kindex,  Lindex] 
                            errSqSum = errSqSum + SqError[Hindex,  Kindex,  Lindex]
                else:
                    minR = sqrt( (float(Hindex)/float(F.shape[0]) - 0.5)**2 + (float(Kindex)/float(F.shape[1]) - 0.5)**2 + (float(Lindex)/float(F.shape[2]) - 0.5)**2)
                    #if minR < 0.1:
                        #return F,  SqError,  0.0, 0.0   
    ratio = float(peakPoints)/float(measuredPoints - peakPoints)
    #print peakSum,  errSqSum,  ratio,  measuredSum,  measuredErrSqSum
    return Peak,  PeakErr2,  peakSum - ratio * (measuredSum - peakSum),  errSqSum + ratio * ratio * (measuredErrSqSum - errSqSum)

def getVanadium(run,  DetCalFile,  workDir, radiusV):
    try:
        sa = Load(workDir+'solidAngle_'+str(run)+'.nxs')
        flux = Load(workDir+'spectra_'+str(run)+'.nxs')
        return sa,  flux
    except:
        # Setting up the workspaces containing information about the flux and the solid angle (from a vanadium run)
        rawVan = Load(Filename = 'TOPAZ_'+str(run)+'_event.nxs')
        LoadIsawDetCal(InputWorkspace = rawVan, Filename = DetCalFile)
        rawVan = AnvredCorrection(InputWorkspace = rawVan, LinearScatteringCoef = 0.367, 
                    LinearAbsorptionCoef = 0.366, Radius = radiusV, OnlySphericalAbsorption = True)
        rawVan = ConvertUnits(InputWorkspace = rawVan, Target = 'Momentum')
        MaskBTP(Workspace = rawVan, Pixel = '0-9, 246-255')
        MaskBTP(Workspace = rawVan, Tube = '0-9, 246-255')
        rawVan = CropWorkspace(InputWorkspace = rawVan, XMin = 1.85, XMax = 10)

        #Solid angle
        sa = Rebin(InputWorkspace = rawVan, Params = '1.85, 10, 10', PreserveEvents = False)
        SaveNexus(InputWorkspace = sa,  Filename = workDir+'solidAngle_'+str(run)+'.nxs')

        #flux
        rawVan = Rebin(InputWorkspace = rawVan, Params = '1.85, 10, 10', PreserveEvents = True)
        banks = CreateGroupingWorkspace(InputWorkspace = rawVan,  GroupDetectorsBy = 'bank')
        SaveDetectorsGrouping(InputWorkspace = "banks",  OutputFile = workDir+'grouping.xml')
        flux = GroupDetectors(InputWorkspace = rawVan, MapFile = workDir+'grouping.xml')
        DeleteWorkspace(rawVan)
        flux = CompressEvents(InputWorkspace = flux, Tolerance = 1e-4)
        flux = Rebin(InputWorkspace = flux, Params = '1.85, 10, 10')
        for i in range(flux.getNumberHistograms()):
          el = flux.getEventList(i)
          el.divide(flux.readY(i)[0], 0)
        flux = Rebin(InputWorkspace = flux, Params = '1.85, 10, 10')
        flux = IntegrateFlux(flux)
        SaveNexus(InputWorkspace = flux,  Filename = workDir+'spectra_'+str(run)+'.nxs')
        return sa,  flux
        
def getSample(run,  UBFile,  DetCalFile,  workDir,  loadDir, formulaSample, radiusSample):
    try:
        MDdata = LoadMD(workDir+'SC2_TOPAZ_'+str(run)+'.nxs')
        return MDdata
    except:
        #data
        data = Load(Filename = loadDir+'TOPAZ_'+str(run)+'_event.nxs')
        LoadIsawDetCal(InputWorkspace = data, Filename = DetCalFile)
        data = FilterBadPulses(InputWorkspace=data, LowerCutoff = 95)
        LoadIsawUB(InputWorkspace = data, Filename = UBFile)
        MDdata = ConvertToMD(InputWorkspace = data, QDimensions = 'Q3D', dEAnalysisMode = 'Elastic', 
          Q3DFrames = 'HKL', QConversionScales = 'HKL', 
          MinValues = '-20, -20, -20', Maxvalues = '20, 20, 20')
        SaveMD(InputWorkspace = MDdata,  Filename = workDir+'MD_TOPAZ_'+str(run)+'.nxs')
        return MDdata

def integrateSample(run,  MDdata,  workDir):
    sample = CreateSampleWorkspace()
    peaks_ws = CreatePeaksWorkspace(InstrumentWorkspace=sample,NumberOfPeaks=4)
    p = peaks_ws.getPeak(0)
    p.setHKL(0,3,3)
    p = peaks_ws.getPeak(1)
    p.setHKL(0,4,4)
    p = peaks_ws.getPeak(2)
    p.setHKL(-2,0,-2)
    p = peaks_ws.getPeak(3)
    p.setHKL(2,0,2)


    #running the algorithm
    p = range(peaks_ws.getNumberPeaks())
    for i in p:
        integratePeak(i, peaks_ws.getPeak(i), sampleRun, MDdata, workDir)
    return peaks_ws
    
def integratePeak(i, peak, run,  MDdata,  workDir):
    H = peak.getH()
    K = peak.getK()
    L = peak.getL()
    Box = IntegrateMDHistoWorkspace(InputWorkspace = 'MDdata',
        P1Bin=str(H-0.25)+',0,'+str(H+0.25),
        P2Bin=str(K-2.0)+',0,'+str(K+2.0),
        P3Bin=str(L-0.25)+',0,'+str(L+0.25),
        OutputWorkspace = 'Box')

    #If you have multiple workspaces,  add separately the output workspaces,  and separately the
    #output normalization workspaces,  then divide the two sums
    SaveMD(InputWorkspace = Box,  Filename = workDir+'MDbox_'+str(run)+'_'+str(i))
    
    PeakBox = CloneMDWorkspace(Box, Outputworkspace = 'MDpeak_'+str(run)+'_'+str(i))
    F = Box.getSignalArray()
    SqError = Box.getErrorSquaredArray()
    Fmax = np.nanmax(F[F<np.inf])
    Fmin = np.nanmin(F[F>0])
    print 'Peak ',  i,  ' Min and Max of Intensity',  Fmin,  Fmax
    minIntensity = Fmin + 0.0001 * (Fmax - Fmin)
    Peak,  PeakErr2,  Intensity,  Err2 = getPeakIntensity(F, SqError,  minIntensity,  10)
    print i,Intensity,Err2
    peak.setIntensity(Intensity)
    peak.setSigmaIntensity(sqrt(Err2))
    PeakBox.setSignalArray(Peak)
    PeakBox.setErrorSquaredArray(PeakErr2)
    MinusBox = MinusMD(LHSWorkspace = Box,  RHSWorkspace = PeakBox,  Outputworkspace = 'MDbkg_'+str(run)+'_'+str(i))

#Only workDir needed
sampleRuns = range(15629,  15630)
formulaSample = 'SC'
radiusSample = 0.0656
vanadiumRun = 15673
radiusV = 0.2
workDir = '/tmp/'

for sampleRun in sampleRuns: 
    MDdata = LoadMD('/SNS/CORELLI/IPTS-17467/shared/20161030_(CaSr)3Ti2O7/normData_Sr0p6.nxs')
    peaks = integrateSample(sampleRun, MDdata, workDir)
    SaveNexus(InputWorkspace = peaks,  Filename = workDir+'peaks_'+str(sampleRun)+'.nxs')
