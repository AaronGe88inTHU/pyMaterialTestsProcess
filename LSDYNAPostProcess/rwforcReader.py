# coding: utf-8
from collections import defaultdict
import numpy as np

def rwforcReader(fileName):
    times = defaultdict(list)
    n_f = defaultdict(list)
    x_f = defaultdict(list)
    y_f = defaultdict(list)
    z_f = defaultdict(list)

    with open(fileName, 'r+') as f:
        #lineCount = len(f.readlines())
        #for ii in range(0, 100)
        for line in f:
        
            res1 = line.split()
            if len(res1) == 6:
                try:
                    [t, k, n ,x, y, z] = res1[:]
                    #print(t, k, n, x, y, z)
                    times[k].append(float(t))
                    n_f[k].append(float(n))
                    x_f[k].append(float(x))
                    y_f[k].append(float(y))
                    z_f[k].append(float(z))
                except ValueError as e:
                    print(str(e))
        return times, n_f, x_f, y_f, z_f
            
            


# res = rwforcReader('JellyRoll_Z.rwforc')
# print(res[0]["1"])