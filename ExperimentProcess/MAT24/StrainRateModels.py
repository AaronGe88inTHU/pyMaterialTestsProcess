import numpy as np
from scipy.optimize import leastsq
import pandas as pd
import PrepareEngineeringCurve

def J_C(x0, plastic_stress_curves):
    A, B, n, c = x0 
    sr = {}
    if '1' in plastic_stress_curves.keys():
        stress = plastic_stress_curves['1']
        plastic_strain = stress[:, 0]
        rate1 = stress[:, 1]
    else:
        k = [ k for k in plastic_stress_curves.keys()][0]
        plastic_strain = plastic_stress_curves[k][:, 0]
        rate1 = np.array(A + B * np.power(plastic_strain, n))

    print(plastic_strain, rate1)
    for r, _ in plastic_stress_curves.items():
        #try:
            sr[r] = np.hstack([plastic_strain.reshape(-1,1), (rate1 * (1 + c * np.log(float(r)))).reshape(-1,1)])

    return sr

def J_C_Model(x0, plastic_stress_curves):
    A, B, n, c = x0 
    #print(plastic_stress_curves.keys())
    if '1' in plastic_stress_curves.keys():
        stress = plastic_stress_curves['1']
        rate1 = stress[:, 1]
    else:
        k = [ k for k in plastic_stress_curves.keys()][0]
        plastic_strain = plastic_stress_curves[k][:, 0]
        rate1 = np.array(A + B * np.power(plastic_strain, n))

    err = []

    for r, s in plastic_stress_curves.items():
        #try:
            sr = rate1 * (1 + c * np.log(float(r)))
            assert len(s) == len(sr)
            err.extend(s[:, 1] - sr)
        #except Exception as identifier:
        #    pass
    #print(err)
    return np.array(err)

class StrainRateSenstivity:
    def __init__(self):
        #self.xlsx_file = xlsx_file
        self.eng_curve_dict = {} # Eng strain-stress curves at strain rates
        
    
    def read_file(self, xlsx_file):
        xlsx = pd.ExcelFile(xlsx_file)
        names = xlsx.sheet_names
        for name in names:
            df = pd.read_excel(xlsx, name)
            #df.replace('--',  0)
            self.eng_curve_dict[name] = df.values

    def to_true_curves(self):
        self.plastic_curve_dic = {}
        if len(self.eng_curve_dict) == 0:
            return None
            #return None
        else:
            
            for k, v in self.eng_curve_dict.items():
                self.plastic_curve_dic[k] = PrepareEngineeringCurve.eng2True(v)

        return self.plastic_curve_dic
            
    def fit_model(self, model, x0):
        if not 'plastic_curve_dic' in self.__dict__:
        
            return None
        else:
            values = self.plastic_curve_dic.values()

            idx = min([value.shape[0] for value in values])
            #for k, v in self.plastic_curve_dic.items():
            stress_curves = {}
            for k, v in self.plastic_curve_dic.items():
                stress_curves[k] = v[:idx, :]


            self.res = leastsq(model, x0, args=stress_curves)
            
            curves = J_C(self.res[0], self.plastic_curve_dic)
            
            return self.res, curves
            


m980 = StrainRateSenstivity()
m980.read_file('980.xlsx')
curves = m980.to_true_curves()
res, new_curves = m980.fit_model(J_C_Model, [1000, 200, 0.1, 1])
print(new_curves)
from matplotlib import pyplot as plt

for k, y in curves.items():
    plt.plot(y[:, 0], y[:, 1], 'y-', label = k, color='r')
for k, y in new_curves.items():
    plt.plot(y[:, 0], y[:, 1], 'y-', label = k, color='b') 
#plt.xlabel('True Strain')
#plt.ylabel('True Stress (MPa)')
plt.legend()
plt.show()