ConvertUnits(InputWorkspace=input, OutputWorkspace=output, Target='dSpacing')
Rebin(InputWorkspace=output, OutputWorkspace=output, Params='0.1, -0.004,10')
SumSpectra(InputWorkspace=output,OutputWorkspace=output)
