
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import pysnooper


# In[44]:


def readForce(fileName, coeff):# direction ='u_c',fileCamera ='Cam1ImageInfo.txt'):
    """
    return
        force_machine, force_sensor 
    """
    csv = pd.read_csv(fileName)
    force_machine = csv.values[1:, 3] * coeff
    force_sensor = csv.values[1:, 4] * coeff
    return force_machine, force_sensor

  
def readDisplacement(direction='u_c'):
    up = pd.read_csv('up')
    disUp = up[direction].values
def readElastic(fileName):
    xlsx = pd.ExcelFile(fileName)
    
    eng = pd.read_excel(xlsx, 'Sheet1')
    return eng.values



readForce('1mps-1.csv', -5164)