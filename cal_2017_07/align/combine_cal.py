from mantid.simpleapi import LoadDiffCal, mtd
import matplotlib.pyplot as plt

LoadDiffCal(Filename='../cal_Si_C60/cal_Si2_47327-47334_TubeCal_sum16_mask_lt_3.cal',
            InstrumentName='CORELLI',
            WorkspaceName='si')

LoadDiffCal(Filename='../cal_Si_C60/cal_C60_2_47367-47382_TubeCal_sum16_mask_lt_3.h5',
            InstrumentName='CORELLI',
            WorkspaceName='c60')

