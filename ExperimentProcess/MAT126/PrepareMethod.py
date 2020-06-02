#!/usr/bin/env python
# coding: utf-8



import numpy as np

import pandas as pd
from collections import namedtuple
import os
import shutil
from ASCIIReader import rwforcReader, rbdoutReader


owd = os.getcwd()

def read_test_results(fileName):
    """
    Read test result from XLSX files
    INPUT:
        fileName
    OUTPUT:
        numpy array of test result curve
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
    

def make_curve(s0, A, n, t):
    """
    Create the target harden curves
    INPUT:
        A, n, s0, t: Curve parameters, seeing manual for details
    
    OUTPUT:
        numpy array of harden curve
    """
    lt_zero = np.arange(-0.2, 0, 0.02)
    lt_zero_stress = -t * lt_zero + s0
    gt_zero = np.arange(0, 2, 0.01)
    gt_zero_stress = A * np.power(gt_zero, n) + s0
    x = np.hstack([lt_zero, gt_zero])
    y = np.hstack([lt_zero_stress, gt_zero_stress])
    return np.hstack([x.reshape(-1,1), y.reshape(-1,1)])




def write_curve(fileName, curve, lcid):
    """
    Create load curve file in *.k 
    INPUT:
        fileName
        curve: numpy file of load curve
        lcid: ID of load curve
    OUTPUT:
        None
    """
    with open(fileName, 'w+') as f:
        f.write("*KEYWORD\n")
        f.write("*DEFINE_CURVE\n")
        f.write("{0}".format(str(int(lcid)))+"\n")
        f.write("$#\n")
        
        for p in curve:
            f.write("{:.4f}, {:.4f}\n".format(p[0], p[1]))

        f.write("*END")




def prepare_files(folder_name, files):
    """
    Copy essential files into target folder
    INPUT:
        folder_name
        files
    """
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    for f in files:
        shutil.copy(os.path.join(owd,f), os.path.join(owd, folder_name, f))#os.path.join(owd,folder_name,f), os.path.join(owd,f))
    os.chdir(folder_name)
    




def execute_calculation(exe_path, main_file):
    """
    execute ls dyna calculation
    INPUT:
        exe_path: lsdyna.exe file path
        main_file: mian *.dyn file
    """
    print(main_file)
    os.system(exe_path + " i=" + main_file + " NCPU=8 Memory=2000m")
    #os.chdir(owd)




def get_result(rgb_id, rw_id, direction = 3):
    """
    Get simulation result
    INPUT:
        rgb_id: ID of Punch
        rw_id: ID of rigid wall
    OUTPUT:
        simulation result
    """
    #print()
    rwf = rwforcReader('rwforc')
    #print(rwf)
    rbd = rbdoutReader('rbdout')
    #print('rwf\n',rwf)
    # print(res[0]['time'], res[1]['2'])
    d_x = np.abs(np.array(rbd[3][str(rgb_id)]).reshape(-1, 1))
    forc = np.array(rwf[1][str(rw_id)]).reshape(-1, 1)
    #print(d_x.shape, forc.shape)
    assert d_x.shape[0] == forc.shape[0]
    return np.hstack([d_x, forc])






