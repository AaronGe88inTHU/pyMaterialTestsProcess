import sys
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit, least_squares
import matplotlib.pyplot as plt
from Constants import five_to_twenty_per

def bracket(x):
    return x if x >= 0 else 0
    
def fun_rate(c, rates, curve0):
    n = len(rates)
    curves = []
    print(c)
    for r in rates:
        curve = (1 + (bracket(np.log(r/c[1])) * c[0])) * curve0
        curves.append(curve)

    return np.array(curves).reshape(-1, n)
    
#def func_CS(c, rates, curve0)
        
def err_rate(c, rates, curves):
    n = len(rates)
    curve0 = curves[0]
    curveRate = np.array(curves).reshape(-1, n)
    fun = fun_rate(c, rates, curve0) - curveRate
    #print(fun,'/n')
    return fun.flatten()

def main(argv):
    fileName = '5182.xlsx'
    xlsx = pd.ExcelFile(fileName)
    names = xlsx.sheet_names
    curves = []
    rates = []
    for name in names:
        df = pd.read_excel(xlsx, name)
        rates.append(float(name))
        print
        curve = df.values[:,1]
        curves.append(curve)

    for curve in curves:
        new_curves = interpolate.interp1d(strain_plastic, stress_plastic, bounds_error=False, fill_value=0.0)
    c0 = (0.1, 1000)
    #print(rates)
    res = least_squares(err_rate, c0, args=(rates, curves))
    print(res)
    c = res.x
    
    curve_s = []
    for r in rates:
        curve = (1 + bracket((np.log(r/c[1]))) * c[0]) * curves[0]
        print(r)
        plt.plot(curve)
        curve_s.append(curve)
    print(np.array(curve_s).shape)
    dfRes = pd.DataFrame(np.array(curve_s).T, columns=['5e-4', '5e-3', '10', '100'])
    dfRes.to_excel('Rt.xlsx', sheet_name='sheet1')
    
    #dfRes = pd.DataFrame(res2, columns=['rFitted', 'tauFitted'])
    #dfRes.to_excel('RYFitted.xlsx', sheet_name='sheet1')
    
    #param = pd.DataFrame(curves, columns=['t', 'q', 'b','h'])
    #param.to_excel('TQBH.xlsx', sheet_name='sheet1')
    plt.show()
    print(c)
    return c

if __name__=="__main__":
    main(sys.argv)
            