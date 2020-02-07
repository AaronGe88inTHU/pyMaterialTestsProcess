import numpy as np
from scipy.optimize import curve_fit

def linear_curve (x, a, b):
        return a * x + b

def fit_linear_elastic(strain, stress):
    opt = curve_fit(linear_curve, strain, stress)
    return opt[0]

def fit_linear_poison(e1, e2):
    opt = curve_fit(linear_curve, e1, e2)
    return -opt[0]