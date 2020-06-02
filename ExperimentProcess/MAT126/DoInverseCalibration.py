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
    res = optimize.least_squares(func, (s, c, n, t), args=([test['sheet1'],]), bounds=([0, 0,1,0], [100, 10000, 2, 1000]),diff_step=[0.05, 0.05, 0.05, 0.05])
    print(res.x)
    #except ValueError as e:
    #    print(res.x)
    #finally:
        #os.chdir(owd)
    return res

test = read_test_results('Z.xlsx')

do_inverse(err_func_step_1_Z, test, [2, 1200, 1.5, 20])