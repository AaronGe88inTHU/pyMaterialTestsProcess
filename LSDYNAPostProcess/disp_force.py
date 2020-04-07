from ASCIIReader import *
import numpy as np





def disp_force(res_file="", direction=0):
    node_info = nodoutReader(res_file+'.nodout')
    assert len(node_info.keys())
    
    #print(node_info.keys())
    d_1 = np.array(node_info[list(node_info.keys())[0]])
    d_2 = np.array(node_info[list(node_info.keys())[1]])
    disp = np.abs((d_1 - d_2)).reshape(-1, 12)[:, direction]
    #print(d_1 - d_2)
    #print(disp.shape[0])

    sec_info = secforReader(res_file+'.secforc')
    #print(node_info.keys())
    assert len(sec_info) == 1
    sec_force = np.array(sec_info[list(sec_info.keys())[0]]).reshape(-1,5)[:, direction+1]
    sec_force = np.abs(sec_force)
    #print(sec_force.shape[0])
    shape = np.min([disp.shape[0], sec_force.shape[0]])
    return np.hstack([disp.reshape(-1,1)[0:shape], sec_force.reshape(-1,1)[0:shape]])

def disp_force_rgdwall(res_file="", direction=3):
    rw_info = rwforcReader(res_file+'.rwforc')[1]
    assert len(rw_info.keys()) == 1
    
    rwforc = np.abs(rw_info[list(rw_info.keys())[0]])

    rgd_info = rbdoutReader(res_file+'.rbdout')[3]

    #print(rgd_info)
    #print(idx)
    idx = np.sort(np.array(list(rgd_info.keys()),dtype=int))[-1]
    #print(idx)
    disp = np.abs(rgd_info[str(idx)])

    shape = np.min([disp.shape[0], rwforc.shape[0]])
    return np.hstack([disp.reshape(-1,1)[0:shape], rwforc.reshape(-1,1)[0:shape]])
    
#df = disp_force_rgdwall('15')
#disp_force([293, 4282], [1])
#print(df)