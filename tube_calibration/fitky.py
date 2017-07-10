from mantid.simpleapi import LoadEventNexus
import numpy as np
import matplotlib.pyplot as plt

COR_47299_23 = LoadEventNexus('/SNS/CORELLI/IPTS-18479/nexus/CORELLI_47299.nxs.h5',BankName='bank23')


def get_detid(bank):
    number = 254*16
    return range((bank-1)*number,bank*number)

