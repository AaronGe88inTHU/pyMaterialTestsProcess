
# coding: utf-8

# In[1]:


import numpy as np
from ReadFile import readTestInfo
import pandas as pd

# In[3]:

def main(argv):
    fileName = argv[1]
    direction = argv[2]
    up = readTestInfo(fileName, 'up.csv', direction)
    down = readTestInfo(fileName, 'down.csv', direction)

    stroke = - up[:,1]+down[:,1]
    result = np.hstack([stroke.reshape(-1,1), up[:,-1].reshape(-1,1)])
    #from matplotlib import pyplot as plt
    #plt.plot(result[:,0], result[:,1])
    #plt.show
    df = pd.DataFrame(result, columns=['stroke', 'force'])
    df.to_excel('sf.xlsx','1')

