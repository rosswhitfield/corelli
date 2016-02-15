g=plotBin("COR_525_offset",0)

l = g.activeLayer()

for i in range(30,61):
	l.setAxisScale(Layer.Bottom,4096*i,4096*(i+1)-1)
	l.setAxisScale(Layer.Left, -0.02,0.02)
	g.exportImage("/SNS/users/rwp/bank"+str(i+1)+".png")

