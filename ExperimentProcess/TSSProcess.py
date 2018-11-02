
# coding: utf-8

# In[1]:


import numpy as np
from ReadFile import readTestInfo


# In[3]:


up = readTestInfo('dows_11.xlsx', 'up.csv', 'u_c')


# In[5]:


down = readTestInfo('dows_11.xlsx', 'down.csv', 'u_c')


# In[8]:


stroke = - up[:,1]+down[:,1]


# In[21]:


stroke


# In[15]:


result = np.hstack([stroke.reshape(-1,1), up[:,-1].reshape(-1,1)])


# In[16]:


result.shape


# In[20]:


from matplotlib import pyplot as plt
plt.plot(result[:,0], result[:,1])
plt.show


# In[23]:


import pandas as pd
df = pd.DataFrame(result, columns=['stroke', 'force'])
df.to_excel('sf.xlsx','1')

