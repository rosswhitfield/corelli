def RotateInstrumentComponentInPlace(Workspace,ComponentName=None, DetectorID=None, X=None, Y=None, Z=None, Angle=None, RelativeRotation=None):
    component = ws.getInstrument().getComponentByName(ComponentName)
    initalPos = component[0].getPos()
    RotateInstrumentComponent(Workspace,ComponentName,DetectorID,X,Y,Z,Angle,RelativeRotation)
    diffPos = initalPos - component[0].getPos()
    MoveInstrumentComponent(Workspace,ComponentName,DetectorID,X=diffPos.getX(),Y=diffPos.getY(),Z=diffPos.getZ())
