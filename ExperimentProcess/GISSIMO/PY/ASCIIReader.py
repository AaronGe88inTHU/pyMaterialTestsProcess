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

def secforReader(fileName):
    k = 0
    idCross = defaultdict(list)
    
    with open(fileName, 'r+') as f:
        #lineCount = len(f.readlines())
        #for ii in range(0, 100)
        for line in f:
            #strip = line.strip()
            #res1 = strip.split()
            #print (len(res1))
            
            
            try:
                res = line.split()
                k = int(res[0])
                #print(k, [float(line[idx[0]: idx[1]]) for idx in idxs])
                #print("ok")
                if len(res)== 6:
                    idCross[k].append(np.array(res[1:6], dtype=float))
                
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
        
    return idCross

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

def rbdoutReader(fileName):
    times = defaultdict(list)
    d_x = defaultdict(list)
    d_y = defaultdict(list)
    d_z = defaultdict(list)
    #timed = False
    k = ""
    local = False
    with open(fileName, 'r+') as f:
        for line in f:
            res1 = line.split()
            if 'time=' in res1:
                times['time'].append(float(res1[-1]))
                #timed = True
            if "rigid" in res1:
                k = res1[-1]
                #print(k)
            if "global" in res1:
                local= False
            if "local" in res1:
                local = True
            if "displacements:" in res1:
                #print('d')
                #print(k)
                if not local:
                    #print(k)
                    d_x[k].append(float(res1[1]))
                    d_y[k].append(float(res1[2]))
                    d_z[k].append(float(res1[3]))
                    #timed = False
    #print(d_z)
    return times, d_x, d_y, d_z


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
