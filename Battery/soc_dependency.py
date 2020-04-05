import numpy as np
from scipy.optimize import leastsq
import pandas as pd
import PrepareCurve
from Constants import zero_to_ten

def expontent_func(x, curves):
    c = x 
    sr = {}

    k = [ k for k in curves.keys()]
    min_k = np.min([float(kk) for kk in k ])
    x = curves[str(int(min_k))][:, 0]
    y = curves[str(int(min_k))][:, 1] 
    # print(y)

    for r, _ in curves.items():
        #try:
            # sr[r] = np.hstack([x.reshape(-1,1), (y * np.exp(c * float(r))).reshape(-1,1)])
            sr[r] = np.hstack([x.reshape(-1,1), (y * (1+c*(float(r)))).reshape(-1,1)])
    return sr

def exponent_dependency(x0, args):
    c = x0
    sr = {}
    curve_soc_0 = args['0']
    # print(args)
    plastic_stress_curves = args
    err = []

    
    for r, s in plastic_stress_curves.items():
        #try:
            if not float(r) == 0.0:
                sr = curve_soc_0[:, 1] * (1 + c*float(r))
                assert len(s) == len(sr)
            
                err.extend(s[:, 1] - sr)

    return err

class SOCDependency:
    def __init__(self, plastic_curve_dic):
  
        self.plastic_curve_dic = plastic_curve_dic
        
    def fit_model(self, model, x0):
        if not 'plastic_curve_dic' in self.__dict__:
        
            return None
        else:
       
            self.res = leastsq(model, x0, args=self.plastic_curve_dic)
            
           
            
            return self.res
    def to_curves(self, func):
        new_curves = func(self.res[0], self.plastic_curve_dic)
        return new_curves

curves = PrepareCurve.read_file('18650.xlsx', zero_to_ten)
print(curves)
#curves_copy = 

b_18650 = SOCDependency(curves)
#curves = m980.to_true_curves()
res = b_18650.fit_model(exponent_dependency, [1])
new_curves = b_18650.to_curves(expontent_func)
print(res)
from matplotlib import pyplot as plt

for k, y in curves.items():
    plt.plot(y[:, 0], y[:, 1], 'y-', label = k, color='r')
#print(curves)
for k, y in new_curves.items():
    plt.plot(y[:, 0], y[:, 1], 'y-', label = k) 
#plt.xlabel('True Strain')
#plt.ylabel('True Stress (MPa)')
plt.legend()
plt.show()