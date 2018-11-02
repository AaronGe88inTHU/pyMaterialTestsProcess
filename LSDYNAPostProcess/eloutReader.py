
# coding: utf-8
from collections import defaultdict
import numpy as np

def eloutReader(fileName):
    idStrain = defaultdict(list)
    with open(fileName, 'r+') as f:
        #lineCount = len(f.readlines())
        #for ii in range(0, 100)
        for line in f:
            strip = line.strip()
            res1 = strip.split(' ')
            if str(res1[0]).endswith('-'):
                theID = int(res1[0].split('-')[0])
                line2 = f.readline()
                if len(line2) > 100:
                    continue
                #res2 = line2.split(' ')
                line2 = line2[17:]
                xx = float(line2[0:12])
                yy = float(line2[12: 24])
                zz = float(line2[24:36])
                xy = float(line2[36:48])
                yz = float(line2[48:60])
                zx = float(line2[60:72])
                
                idStrain[theID].append([xx, yy, zz, xy, yz, zx])
                #value = float(res2[-4])
                #idMises[theID] = value
    return idStrain

def effectStrain(strain):
    tensor = np.zeros([3,3])#np.array(strain).reshape([-1, 3])
    tensor[0,0] = strain[0]
    tensor[1,1] = strain[1]
    tensor[2,2] = strain[2]
    tensor[0,1] = strain[3]
    tensor[1,0] = strain[3]
    tensor[2,0] = strain[5]
    tensor[0,2] = strain[5]
    tensor[1,2] = strain[4]
    tensor[2,1] = strain[4]
    principle,_ = np.linalg.eig(tensor)
    #print(principle)
    divTensor = tensor - 1 / 3 * np.sum(principle) * np.diag([1,1,1])
    J2 = 0.5 * (divTensor[0, 0] ** 2 + divTensor[1, 1] ** 2 + divTensor[2, 2] ** 2)
    effectStrain = np.sqrt(4/3*J2)
    return effectStrain
