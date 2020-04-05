# coding: utf-8
from collections import defaultdict
import numpy as np

def nodoutReader(fileName):
    k = 0
    idNode = defaultdict(list)
    
    with open(fileName, 'r+') as f:
        #lineCount = len(f.readlines())
        #for ii in range(0, 100)
        for line in f:
            #strip = line.strip()
            #res1 = strip.split()
            #print (len(res1))
            
            
            try:
                k = int(line[0:10])
                
                idxs = [[10+ii*12, 10+(ii+1)*12] for ii in range(0, 12)]
                
                #print(k, [float(line[idx[0]: idx[1]]) for idx in idxs])
                #print("ok")
                idNode[k].append([float(line[idx[0]: idx[1]]) for idx in idxs])
                    

            except Exception as e:
                pass
             
                
            # if str(res1[0]).endswith('-'):
            #     theID = int(res1[0].split('-')[0])
            #     line2 = f.readline()
            #     if len(line2) > 100:
            #         continue
            #     #res2 = line2.split(' ')
            #     line2 = line2[17:]
            #     xx = float(line2[0:12])
            #     yy = float(line2[12: 24])
            #     zz = float(line2[24:36])
            #     xy = float(line2[36:48])
            #     yz = float(line2[48:60])
            #     zx = float(line2[60:72])
                
            #     idStrain[theID].append([xx, yy, zz, xy, yz, zx])
            #     #value = float(res2[-4])
            #     #idMises[theID] = value
        
    return idNode


