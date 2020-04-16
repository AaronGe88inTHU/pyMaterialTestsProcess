
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from scipy import interpolate


# In[44]:


def readTestInfo(fileMachine, fileDic, direction ='u_c',fileCamera ='Cam1ImageInfo.txt'):
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
        if df.shape[0] > 20:
            test = name
            break
    machine = pd.read_excel(xlsx, test)
    machine = machine[2:].values
    machineTime = machine[:, 2].astype(float)
    force = machine[:,1].astype(float)
    
    
    camera = pd.read_csv(fileCamera, header=None)
    cameraTime = camera.loc[:, 1].values.reshape(-1,1).astype(float)


    dic = pd.read_csv(fileDic)
    result = dic[direction].values.reshape(-1,1).astype(float)
    count = np.min([np.max(result.shape[0]), np.max(cameraTime.shape[0])])    
    cameraTime = cameraTime[0:count]
    result = result[0:count]

    print(cameraTime.shape, result.shape)
    funcCamera = interpolate.interp1d(cameraTime.flatten(), result.flatten(), bounds_error=False)
    funcMachine = interpolate.interp1d(machineTime.flatten(), force.flatten(), bounds_error=False) 
    
 
    the_time = np.min([np.max(cameraTime), np.max(machineTime)])
    time_range = np.linspace(0, the_time, 2000)
    the_camera = funcCamera(time_range)
    the_force = funcMachine(time_range)

    return np.hstack([time_range.reshape(-1,1), the_camera.reshape(-1,1), the_force.reshape(-1,1)])


def readElastic(fileName):
    xlsx = pd.ExcelFile(fileName)
    
    eng = pd.read_excel(xlsx, 'Sheet1')
    return eng.values



