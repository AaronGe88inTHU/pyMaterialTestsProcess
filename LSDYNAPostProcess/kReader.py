
# coding: utf-8

# In[1]:


from collections import defaultdict
from eloutReader import eloutReader


# In[55]:


def setLoader(fileName):
    elementSet = defaultdict(list)
    with open(fileName, 'r+') as f:
        for line in f:
            if line.startswith('*SET_SOLID'):
                while 1:
                    setName = f.readline().strip()
                    if setName.endswith('END'):
                        break
                
                    elif setName.endswith('MECH'):
                        setElement = []
                        while 1:
                            sets = f.readline()
                            #print(sets)
                            if sets.startswith('$'):
                                if len(sets.strip()) > 20:
                                    continue
                                else:
                                    break
                                #print(setElement)
                            else:
                                #print(sets)
                                #print(sets)
                                for ii in range(8):
                                    setElement.append(int(sets[ii*10:ii*10+10]))
                                
                        setName = int(setName.split('M')[0])
                        elementSet[setName].append(setElement)
                        comment = f.readline()
                        if comment.startswith('$') or comment.endswith('END'):
                            break
            
    return elementSet
                            
                            


# In[61]:


ele = setLoader('cone_s_withset_2.k')
ele.keys()

