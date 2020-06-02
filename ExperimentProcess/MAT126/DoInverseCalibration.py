#!/usr/bin/env python
# coding: utf-8

import numpy as np
from scipy import optimize, interpolate
from Step_1_Z import err_func_step_1_Z
from PrepareMethod import read_test_results
from scipy import optimize


def do_inverse(func, test, init_param):
    """
    Main function of optimizing process using least squares method
    INPUT:
        test: test result
        init_param: initial parameters
    OUTPUT:
        res: optimized paramter
    """
    print(test)
    #try:
    s, c, n, t = init_param[:4]
    res = optimize.minimize(func, (s, c, n, t), args=([test['sheet1'],]), method='L-BFGS-B', bounds=([0, 100],[0, 5000], [0.1, 5],[5, 1000]), options={"eps":0.01})
    print(res.x)
    #except ValueError as e:
    #    print(res.x)
    #finally:
        #os.chdir(owd)
    return res

test = read_test_results('Z.xlsx')

do_inverse(err_func_step_1_Z, test, [0.1, 500, 1.5, 200])