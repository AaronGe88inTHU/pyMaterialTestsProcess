# coding: utf-8
from collections import defaultdict
import numpy as np

def rbdoutReader(fileName):
    times = defaultdict(list)
    d_x = defaultdict(list)
    d_y = defaultdict(list)
    d_z = defaultdict(list)
    timed = False
    k = ""
    with open(fileName, 'r+') as f:
        for line in f:
            res1 = line.split()
            if 'time=' in res1:
                times['time'].append(float(res1[-1]))
                timed = True
            if "rigid" in res1:
                k = res1[-1]
                #print(k)
            if "displacements:" in res1:
                print('d')
                if timed:
                    d_x[k].append(float(res1[1]))
                    d_y[k].append(float(res1[2]))
                    d_z[k].append(float(res1[3]))
                    timed = False

    return times, d_x, d_y, d_z

res = rbdoutReader('JellyRoll_Z.rbdout')
print(res[0]['time'], res[1]['2'])