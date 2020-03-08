import numpy as np
from scipy.optimize import leastsq
import pandas as pd
import PrepareEngineeringCurve

def J_C(x0, plastic_stress_curves):
    A, B, n, c = x0 
    sr = {}
    # if '1' in plastic_stress_curves.keys():
    #     # stress = plastic_stress_curves['1']
    #     # plastic_strain = stress[:, 0]
    #     # rate1 = stress[:, 1]
    #     pass
    # else:
    k = [ k for k in plastic_stress_curves.keys()][0]
    plastic_strain = plastic_stress_curves[k][:, 0]
    rate1 = np.array(A + B * np.power(plastic_strain, n))

    #print(plastic_strain, rate1)
    for r, _ in plastic_stress_curves.items():
        #try:
            sr[r] = np.hstack([plastic_strain.reshape(-1,1), (rate1 * (1 + c * np.log(float(r)))).reshape(-1,1)])

    return sr

def C_S(x0, plastic_stress_curves):
    A, B, n, d1, d2 = x0 
    sr = {}
    # if '1' in plastic_stress_curves.keys():
    #     # stress = plastic_stress_curves['1']
    #     # plastic_strain = stress[:, 0]
    #     # rate1 = stress[:, 1]
    #     pass
    # else:
    k = [ k for k in plastic_stress_curves.keys()]
    min_k = np.min([float(kk) for kk in k ])
    plastic_strain = plastic_stress_curves[str(min_k)][:, 0]
    rate1 = np.array(A + B * np.power(plastic_strain, n))
    #rate_low = plastic_stress_curves[str]    
    

    #print(plastic_strain, rate1)
    for r, _ in plastic_stress_curves.items():
        #try:
            sr[r] = np.hstack([plastic_strain.reshape(-1,1), ( rate1 * (1 + np.power((float(r) * d1), d2))).reshape(-1,1)])
    return sr

# def Double_C_S(x0, plastic_stress_curves):
#     pass


def J_C_Model(x0, plastic_stress_curves):
    A, B, n, c = x0 
    #print(plastic_stress_curves.keys())
    err = []
    # if '1' in plastic_stress_curves.keys():
    #     stress = plastic_stress_curves['1']
    #     rate1 = stress[:, 1]
    #     for r, s in plastic_stress_curves.items():
    #         if not r == "1":
    #             sr = rate1 * (1 + c * np.log(float(r)))
    #             assert len(s) == len(sr)
    #             err.extend(s[:, 1] - sr)
    # else:
    k = [ k for k in plastic_stress_curves.keys()][0]
    plastic_strain = plastic_stress_curves[k][:, 0]
    #rate1 = np.array(A + B * np.power(plastic_strain, n))
    for r, s in plastic_stress_curves.items():
        #try:
        sr = rate1 * (1 + c * np.log(float(r)))
        assert len(s) == len(sr)
        err.extend(s[:, 1] - sr)
    
        #except Exception as identifier:
        #    pass
    #print(err)
    return np.array(err)

    

def C_S_Model(x0, plastic_stress_curves):
    A, B, n, d1, d2 = x0 
    #print(plastic_stress_curves.keys())
    err = []
    # if '1' in plastic_stress_curves.keys():
    #     stress = plastic_stress_curves['1']
    #     rate1 = stress[:, 1]
    #     for r, s in plastic_stress_curves.items():
    #         if not r == "1":
    #             sr = rate1 * (1 + c * np.log(float(r)))
    #             assert len(s) == len(sr)
    #             err.extend(s[:, 1] - sr)
    # else:
    k = [ k for k in plastic_stress_curves.keys()][0]
    plastic_strain = plastic_stress_curves[k][:, 0]
    rate1 = np.array(A + B * np.power(plastic_strain, n))
    for r, s in plastic_stress_curves.items():
        #try:
        sr = rate1 * (1 + np.power(float(r) * d1, d2))
        assert len(s) == len(sr)
        err.extend(s[:, 1] - sr)
    
        #except Exception as identifier:
        #    pass
    #print(err)
    return np.array(err)

# def Double_C_S_Model(x0, plastic_stress_curves):
#     A, B, n, d1, d2 = x0 
#     #print(plastic_stress_curves.keys())
#     err = []
#     # if '1' in plastic_stress_curves.keys():
#     #     stress = plastic_stress_curves['1']
#     #     rate1 = stress[:, 1]
#     #     for r, s in plastic_stress_curves.items():
#     #         if not r == "1":
#     #             sr = rate1 * (1 + c * np.log(float(r)))
#     #             assert len(s) == len(sr)
#     #             err.extend(s[:, 1] - sr)
#     # else:
#     k = [ k for k in plastic_stress_curves.keys()][0]
#     plastic_strain = plastic_stress_curves[k][:, 0]
#     rate1 = np.array(A + B * np.power(plastic_strain, n))
#     for r, s in plastic_stress_curves.items():
#         #try:
#         sr = rate1 * (1 + np.power(float(r) * d1, d2))
#         assert len(s) == len(sr)
#         err.extend(s[:, 1] - sr)
    
#         #except Exception as identifier:
#         #    pass
#     #print(err)
#     return np.array(err)



class StrainRateSenstivity:
    def __init__(self, plastic_curve_dic):
        #self.xlsx_file = xlsx_file
        #self.eng_curve_dict = {} # Eng strain-stress curves at strain rates
        self.plastic_curve_dic = plastic_curve_dic
    def fit_model(self, model, x0):
        if not 'plastic_curve_dic' in self.__dict__:
        
            return None
        else:
            #values = self.plastic_curve_dic.values()

           
            #for k, v in self.plastic_curve_dic.items():
            #stress_curves = {}
            #for k, v in self.plastic_curve_dic.items():
            #    stress_curves[k] = v[idxmin:idxmax, :]
            self.res = leastsq(model, x0, args=self.plastic_curve_dic)
            
           
            
            return self.res
    def to_curves(self, func):
        new_curves = func(self.res[0], self.plastic_curve_dic)
        return new_curves

curves = PrepareEngineeringCurve.read_plastic_file('5182.xlsx')
GC420 = StrainRateSenstivity(curves)
#curves = m980.to_true_curves()
res = GC420.fit_model(C_S_Model, [1000, 200, 0.1, 0.01, 5])
new_curves = GC420.to_curves(C_S)
print(res)
from matplotlib import pyplot as plt

for k, y in curves.items():
    plt.plot(y[:, 0], y[:, 1], 'y-', label = k, color='r')
for k, y in new_curves.items():
    plt.plot(y[:, 0], y[:, 1], 'y-', label = k, color='b') 
#plt.xlabel('True Strain')
#plt.ylabel('True Stress (MPa)')
plt.legend()
plt.show()