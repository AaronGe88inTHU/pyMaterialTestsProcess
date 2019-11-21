
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from scipy import interpolate


# In[44]:


def readTestInfo(fileMachine, fileDic, direction ='u_c',fileCamera ='0_048mmpermin-1.csv'):
    """
    return
        time
        result
        force
    """
    xlsx = pd.ExcelFile(fileMachine)
    names = xlsx.sheet_names
    test = ''
    for name in names:
        df = pd.read_excel(xlsx, name)
        #print(df.shape)
        if df.shape[0] > 20:
            test = name
            break
    machine = pd.read_excel(xlsx, test)
    machine = machine[0:].values
    machineTime = machine[:, 2].astype(float)
    force = machine[:,10].astype(float)
    
    
    #camera = machineTime
    cameraTime = machineTime#camera.loc[2:, 2].values.reshape(-1,1).astype(float)
    #print(cameraTime)
    dic = pd.read_csv(fileDic)
    resultEx = dic[direction].values.reshape(-1,1).astype(float)
    count = resultEx.shape[0]
    print(cameraTime.shape[0], count)
    cameraTime = cameraTime[:] - cameraTime[0]
    #print (cameraTime)
    #timeResult = np.hstack([cameraTime, result]).reshape(-1, 2)
    #print(cameraTime.shape, result.shape)
    #funcEx = interpolate.interp1d(cameraTime[:,0], result[:,0], bounds_error=False)
    
    #machineTime = machineTime.reshape(-1,1)
    #machineTime = machineTime[:,0]
    #resultEx = np.array([funcEx(t) for t in machineTime])
    #resultEx = funcEx(machineTime.reshape(-1, 1))
    #print(machineTime.shape, resultEx.shape, force.shape)
    #nan = np.isnan(resultEx)
    #resultEx = resultEx[~nan]
    #machineTime = machineTime[~nan]
    #force = force[~nan]
    #print(machineTime.shape, resultEx.shape, force.shape)
    print(machineTime.shape, resultEx.shape, force.shape)
    return np.hstack([machineTime[:count].reshape(-1,1), resultEx, force[:count].reshape(-1,1)]).reshape(-1, 3)


def readElastic(fileName):
    xlsx = pd.ExcelFile(fileName)
    
    eng = pd.read_excel(xlsx, 'Sheet1')
    return eng.values



