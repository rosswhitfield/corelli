# use cc data rather than raw data to generate SA and spectrum.

filedir="/SNS/CORELLI/IPTS-15796/nexus/"
outputdir = "/SNS/CORELLI/shared/Vanadium/"
ccfiledir = "/SNS/CORELLI/IPTS-15796/shared/autoreduce/"

# Vanadium
runs = range(27823, 27828, 1)
#runs = [27823]

# PrAl3
#runs = range(30338,30346)
#runs = [30338]

files='+'.join([filedir+'CORELLI_'+str(r)+'.nxs.h5' for r in runs])

van = Load(Filename= files)

#Mask the detector as of July 16, 2016 after the summer break
# -- edge pixels
MaskBTP(Workspace='van',Bank="1-29", Pixel="1-14,244-256")    #  detector edges, Row A
MaskBTP(Workspace='van',Bank="30-62", Pixel="1-13,244-256")    #  detector edges, Row A
MaskBTP(Workspace='van',Bank="63-91", Pixel="1-14,243-256")    #  detector edges, Row A

# -- uninstalled modules
MaskBTP(Workspace='van',Bank="1-6,29,30,62-68,91")     # uninstalled modules

# bad tubes and pixels
MaskBTP(Workspace='van',Bank="7",Tube="4", Pixel="1-32")   #Bad pixels
MaskBTP(Workspace='van',Bank="14",Tube="8-16", Pixel="1-18")   #Bad pixels
MaskBTP(Workspace='van',Bank="15",Tube="8")
MaskBTP(Workspace='van',Bank="18",Tube="6")
MaskBTP(Workspace='van',Bank="26",Tube="9-16", Pixel="237-256")   #Bad pixels
MaskBTP(Workspace='van',Bank="27",Tube="10", Pixel="1-16")   #Bad pixels
MaskBTP(Workspace='van',Bank="45",Tube="15")   
MaskBTP(Workspace='van',Bank="47",Tube="16", Pixel="1-18")   #Bad pixels
MaskBTP(Workspace='van',Bank="49",Tube="1")
MaskBTP(Workspace='van',Bank="51",Tube="2", Pixel="242-256")   #Bad pixels
MaskBTP(Workspace='van',Bank="73",Tube="11")   
MaskBTP(Workspace='van',Bank="80",Tube="6")

# -- DB
MaskBTP(Workspace='van',Bank="58",Tube="13-16",Pixel="80-130")   #DB
MaskBTP(Workspace='van',Bank="59",Tube="1-4",Pixel="80-130")       #DB

SortEvents(InputWorkspace='van',SortBy="Pulse Time + TOF")
vanCC = CorelliCrossCorrelate('van', 56000)

def momentumtd(angle,params):
    ConvertUnits(InputWorkspace='van', OutputWorkspace='q', Target='MomentumTransfer')
    ConvertUnits(InputWorkspace='vanCC', OutputWorkspace='qCC', Target='MomentumTransfer')
    MaskAngle('q',MinAngle=0,MaxAngle=angle-2)
    MaskAngle('q',MinAngle=angle+2,MaxAngle=180)
    MaskAngle('qCC',MinAngle=0,MaxAngle=angle-2)
    MaskAngle('qCC',MinAngle=angle+2,MaxAngle=180)
    Rebin(InputWorkspace='q', OutputWorkspace='q', Params=params, PreserveEvents=False)
    Rebin(InputWorkspace='qCC', OutputWorkspace='qCC', Params=params, PreserveEvents=False)
    SumSpectra(InputWorkspace='q', OutputWorkspace='q_'+str(angle))
    SumSpectra(InputWorkspace='qCC', OutputWorkspace='qCC_'+str(angle))
    Divide(LHSWorkspace='qCC_'+str(angle),RHSWorkspace='q_'+str(angle),OutputWorkspace=str(angle))

momentumtd(40,'1.5,0.01,7')
momentumtd(65,'2,0.01,12')
momentumtd(90,'3,0.01,15')
momentumtd(115,'4,0.01,18')
momentumtd(140,'4,0.01,20')
