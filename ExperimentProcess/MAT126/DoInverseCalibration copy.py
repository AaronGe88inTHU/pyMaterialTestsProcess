#!/usr/bin/env python
# coding: utf-8

import numpy as np
from scipy import optimize, interpolate
from Step_1_Z import err_func_step_1_Z

owd = os.getcwd()

def do_inverse(func, test, init_param,):
    """
    Main function of optimizing process using least squares method
    INPUT:
        test: test result
        init_param: initial parameters
    OUTPUT:
        res: optimized paramter
    """
    #print(test)
    #try:
    s, c, n = init_param[:3]
    res = optimize.least_squares(func, (s, c, n), args=([test['sheet1'],]), bounds=([0, 1, 1], [np.inf, np.inf, np.inf]))
    print(res.x)
    #except ValueError as e:
    #    print(res.x)
    #finally:
        #os.chdir(owd)
    return res

test = read_test_results('X.xlsx')
cur_num = 1
