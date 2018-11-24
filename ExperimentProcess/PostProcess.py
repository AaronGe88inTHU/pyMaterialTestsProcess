
# coding: utf-8

# In[4]:

import sys
import numpy as np
from ReadFile import readTestInfo
from matplotlib import pyplot as plt
import pandas as pd


# In[5]:


def strokeForce(fileName, direction):
    up = readTestInfo(fileName, 'up.csv', direction)
    down = readTestInfo(fileName, 'down.csv', direction)
    stroke =  up[:,1]-down[:,1]
    result = np.hstack([stroke.reshape(-1,1), up[:,-1].reshape(-1,1)])
    plt.plot(result[:,0], result[:,1])
    plt.show()
    df = pd.DataFrame(result, columns=['stroke', 'force'])
    df.to_excel('sf.xlsx','1')

def strainStress(fileName, width, thick):
    e1 = readTestInfo(fileName, 'strain.csv', 'e1')
    e2 = readTestInfo(fileName, 'strain.csv', 'e2')
    em = readTestInfo(fileName, 'strain.csv', 'e_vonmises')
    
    def trueStrain(force, e1, width, thick):
        return force / (width * thick) * (1 + e1)

    sig = trueStrain(e1[:, 2], e1[:, 1], width, thick)
    result = np.hstack([e1[:,1].reshape(-1,1), e2[:,1].reshape(-1,1), em[:, 1].reshape(-1,1), sig.reshape(-1,1)])
    plt.plot(result[:,0], result[:,3])
    plt.show()

    df = pd.DataFrame(result, columns=['e1','e2','em', 'sig'])
    df.to_excel('harden.xlsx','1')
    
# In[6]:

def main(argv):
    if argv == None:
        print('world~!')
    else:
        print(argv)
        fileName, width, thick, direction = argv[1:5]
        strainStress(fileName, float(width), float(thick))
        strokeForce(fileName, direction)
        
if __name__=="__main__":
    main(sys.argv)
    



# In[21]:





# In[16]:





# In[20]:





# In[23]:




