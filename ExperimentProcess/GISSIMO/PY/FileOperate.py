import numpy as np
import pandas as pd
import logging
import os
from scipy import interpolate

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
    labels = []
    for sheet in xlsx.sheet_names:
        #print(sheet)
        df = pd.read_excel(xlsx, sheet)
        eta = df.loc[:, 'TRI'].values.reshape(-1, 1)
        thetaBar = -df.loc[:, 'LP'].values.reshape(-1, 1)
        eplison = df.loc[:, 'EPS'].values.reshape(-1, 1)
        ind = np.where(eplison>0)
        #print(sheet)
        #print(ind)
        ete = np.hstack([eta, thetaBar, eplison])
        
        etaThetaEpsilon.append(ete[ind[0],:])
        labels.append(sheet)
    
    #logging.debug(etaThetaEpsilon)
    etaThetaEpsilon = np.array(etaThetaEpsilon)
    return etaThetaEpsilon, labels
    
def preProcess(cwd):
    fileNames = os.listdir(cwd)
    clearedData = pd.ExcelWriter('clearedData.xlsx')
    for f in fileNames:
        if os.path.splitext(f)[1] == '.xlsx':
            ff = os.path.join('data', f)
            df = pd.read_excel(ff, 'Sheet1')
            time = df.loc[:,'TIME'].values[1:]
            time1 = df.loc[:, 'TIME.1'].values[1:]
            
            time = np.array(time)[~np.isnan(time)]
            time1 = np.array(time1)[~np.isnan(time1)]
            
            (timeEps, timeLP) = (time, time1) if len(time) < len(time1) else (time1, time)
            eps = df.loc[:, 'EPS'].values[1:]
            eps = np.array(eps)[~np.isnan(eps)]
            
            #timeLP = np.array(timeLP)[np.where(timeLP < np.max(timeEps))]
            #wprint(timeLP)
            timeLP = timeLP[timeLP < np.max(timeEps)]
            funcInterp = interpolate.interp1d(timeEps, eps, bounds_error=None)
            epsFullLength = funcInterp(timeLP).reshape(-1,1)
            timeLP = timeLP.reshape(-1,1)
            LP = df.loc[:,'LP'].values[1:]
            LP = LP[0:len(timeLP)].reshape(-1,1)
            
            TRI = df.loc[:,'TRI'].values[1:]
            TRI = TRI[0:len(timeLP)].reshape(-1, 1)

            data = np.hstack([timeLP, epsFullLength, LP, TRI])
            dff = pd.DataFrame(data, columns=['TIME', 'EPS', 'LP', 'TRI'])
            dff.to_excel(clearedData, sheet_name=os.path.splitext(f)[0])
    clearedData.save()
'''
tests = readXlsx('clearedData.xlsx')

import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

fig = plt.figure()

ax = fig.gca(projection='3d')
plots = []
labels = []
ii = 0
for test in tests:
    xx, yy, zz = test[:, 0], test[:, 1], test[:, 2]
    pl = ax.plot(xx, yy, zz, label=str(ii))#, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    plots.append(pl)
    labels.append(str(ii))
    ii = ii + 1
    
ax.legend()#
ax.xaxis.set_major_locator(LinearLocator(5))
ax.yaxis.set_major_locator(LinearLocator(5))
ax.set_xlabel('Triaxiality')
ax.set_ylabel('Lode Parameter')
ax.set_zlabel('Failure plastic strain')

plt.show()
'''