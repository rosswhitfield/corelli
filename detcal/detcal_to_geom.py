from mantid.simpleapi import LoadEmptyInstrument, LoadIsawDetCal

cor = LoadEmptyInstrument(InstrumentName='CORELLI')
LoadIsawDetCal(cor, 'SCD_Grouped_calib.results')

i=cor.getInstrument()

def mapBankToABC(i):
    if i<30:
        return "A"+str(i)
    elif i<63:
        return "B"+str(i-29)
    else:
        return "C"+str(i-62)

print "Location Xsci Ysci Zsci Xrot_sci Yrot_sci Zrot_sci"

for bank in range(1,92):
    b=i.getComponentByName("bank"+str(bank)+"/sixteenpack")
    x=b.getPos().getX()*1000
    y=b.getPos().getY()*1000
    z=b.getPos().getZ()*1000
    [beta,alpha,gamma]=b.getRotation().getEulerAngles("YXZ")
    print mapBankToABC(bank),x,y,z,alpha,beta,gamma
