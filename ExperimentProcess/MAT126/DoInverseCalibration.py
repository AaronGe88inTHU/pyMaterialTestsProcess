#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from scipy import optimize, interpolate
import pandas as pd
from collections import namedtuple
import os
import shutil
from ASCIIReader import rwforcReader, rbdoutReader


# In[2]:


def read_test_results(fileName):
    """
    ToDO
    """
    tests_dict = {}
    excel = pd.ExcelFile(fileName)
    for sheet in excel.sheet_names:
        df = excel.parse(sheet)
        value = df.values
        #print(sheet)
        #print(value.shape)
        tests_dict[sheet] = value
    return tests_dict
    


# In[3]:





# In[4]:


def make_curve(A, n, s0):
    """
    TODO
    """
    lt_zero = np.arange(-0.2, 0, 0.02)
    lt_zero_stress = -80 * lt_zero + s0
    gt_zero = np.arange(0, 2, 0.01)
    gt_zero_stress = A * np.power(gt_zero, n) + s0
    x = np.hstack([lt_zero, gt_zero])
    y = np.hstack([lt_zero_stress, gt_zero_stress])
    return np.hstack([x.reshape(-1,1), y.reshape(-1,1)])


# In[5]:


def write_curve(fileName, curve, lcid):
    """
    TODO
    """
    with open(fileName, 'w+') as f:
        f.write("*KEYWORD\n")
        f.write("*DEFINE_CURVE\n")
        f.write("{0}".format(str(int(lcid)))+"\n")
        f.write("$#\n")
        
        for p in curve:
            f.write("{:.4f}, {:.4f}\n".format(p[0], p[1]))

        f.write("*END")


# In[6]:


def prepare_files(folder_name, files):
    """
    TODO
    """
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for f in files:
        shutil.copy(os.path.join(owd,f), os.path.join(owd, folder_name, f))#os.path.join(owd,folder_name,f), os.path.join(owd,f))
    os.chdir(folder_name)
    


# In[7]:


def execute_calculation(exe_path, main_file):
    os.system(exe_path + " i=" + main_file + " NCPU=8 Memory=2000m")
    os.chdir


# In[8]:


def get_result(rgb_id, rw_id):
    """
    TODO
    """
    rwf = rwforcReader('rwforc')
    #print(res[0]["1"])# 
    rbd = rbdoutReader('rbdout')
    # print(res[0]['time'], res[1]['2'])
    d_x = np.abs(np.array(rbd[1][str(rgb_id)]).reshape(-1, 1))
    forc = np.array(rwf[1][str(rw_id)]).reshape(-1, 1)
    #print(d_x.shape, forc.shape)
    assert d_x.shape[0] == forc.shape[0]
    return np.hstack([d_x, forc])


# In[9]:


def func_simulation(param):
    """
    TODO
    """
    global cur_num
    with open ("param.txt", "a+") as f:
        f.write("{0:d},{1:.4f},{2:.4f}, {3:.4f}\n".format(cur_num, param[0], param[1], param[2]))
    curve = make_curve(param[0], param[1], param[2])
    prepare_files(str(cur_num), ['JellyRoll.blk', 'JellyRoll.mat', 'cylinder.k', 'X-D50.dyn', '2200.k','2300.k'])
    write_curve('2100.k', curve, 2100)
    #execute_calculation('D:\LSDYNA\program\ls-dyna_smp_s_R11_0_winx64_ifort131.exe', 'XSphD25.dyn')
    simu = get_result(3, 3)
    #print(simu)
    os.chdir(owd)
    cur_num += 1
    return simu

def err_func(param, args):
    #print(param)
    #print(args)
    test = np.array(args)
    #print(test)
    simu = func_simulation(param)
    funcSim = interpolate.interp1d(simu[:,0], simu[:,1], bounds_error=False)
    print(simu)
    funcTest = interpolate.interp1d(test[:,0], test[:,1], bounds_error=False)
    if np.max(test[:,0]) > np.max(simu[:,0]):
        top = np.max(simu[:,0])
    else:
        top = np.max(test[:,0])
    #print(top)
    if np.min(test[:,0]) > np.min(simu[:,0]):
        lower = np.min(test[:,0])
    else:
        lower = np.min(simu[:,0])
    
    inter_sim = funcSim(np.arange(lower,top, 0.001))
    inter_test = funcTest(np.arange(lower,top, 0.001))
    #print(inter_sim)
    return inter_sim - inter_test


def do_inverse(test):
    """
    TODO
    """
    #print(test)
    #try:
    res = optimize.least_squares(err_func, (60, 1.67, 0.2), args=([test['df2'],]),)# bounds=(np.inf, np.inf, np.inf))
    print(res.x)
    #except ValueError as e:
    #    print(res.x)
    #finally:
        #os.chdir(owd)
    return res


# In[ ]:

test = read_test_results('X.xlsx')
cur_num = 1
owd = os.getcwd()
do_inverse(test)


# In[ ]:




