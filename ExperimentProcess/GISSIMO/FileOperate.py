import numpy as np
import pandas as pd
import logging

def readXlsx(fileName):
    """
    read all sheets in xls file
    input:
        fileName
    output:
        listEta, listThetaBar, listEpsilon in sheets
    """
    xlsx = pd.ExcelFile(fileName)
    etaThetaEpsilon = []
    for sheet in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet)
        eta = df.ix[:, 'eta'].values.reshape(-1, 1)
        thetaBar = df.ix[:, 'thetaBar'].values.reshape(-1, 1)
        eplison = df.ix[:, 'epsilon'].values.reshape(-1, 1)
        ete = np.hstack([eta, thetaBar, eplison])
        etaThetaEpsilon.append(ete)
    
    logging.debug(etaThetaEpsilon)
    return np.array(etaThetaEpsilon)