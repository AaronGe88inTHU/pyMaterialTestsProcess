#!/usr/bin/env python
# coding: utf-8
import numpy as np
import os
from PrepareMethod import make_curve, prepare_files, write_curve, execute_calculation, get_result, owd
from scipy import interpolate


cur_num = 1
exe_path = "D:\\LSDYNA7\\program\\ls-dyna_smp_s_R700_winx64_ifort101.exe"


def func_simulation_step_1_Z(param):
    """
    Function for optimization using simulation
    write parameter to param.txt, make loading curve, execute simulation and get result
    INPUT:
        param: optimized paramters
    OUTPUT:
        simu: simulation result
    """
    global cur_num, exe_path, owd
    with open ("param.txt", "a+") as f:
        f.write("{0:d},{1:.4f},{2:.4f}, {3:.4f}, {4:.4f}\n".format(cur_num, param[0], param[1], param[2], param[3]))
    
    c_2300 = make_curve(param[0], param[1], param[2], 2)
    c_2200 = make_curve(2, 22, 1, 20)
    c_2100 = make_curve(2, 12, 1, param[3])

    prepare_files(str(cur_num), ['JellyRoll.blk', 'JellyRoll.mat', 'cylinder.k', 'Z-D50.dyn'])
    write_curve('2100.k', c_2100, 2100)
    write_curve('2200.k', c_2200, 2200)
    write_curve('2300.k', c_2300, 2300)
    execute_calculation(exe_path, "Z-D50.dyn")
    simu = get_result(3, 3)
    #print(simu)
    os.chdir(owd)
    cur_num += 1
    return simu

def err_func_step_1_Z(param, args):
    """
    Function for least square optimization
    INPUT:
        param: optimized paramters
        arges
    OUTPUT:
        err
    """
    test = np.array(args)
    #print(test)
    simu = func_simulation_step_1_Z(param)
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







