import numpy as np
import pandas as pd
from scipy import interpolate
#from Constants import strain_for_interlopating, five_to_twenty_per

def eng2True(curve, E = 207000):
    idx = np.argmax(curve[:, 1])
    eng = curve[:idx,:]
    
    strain_true = np.log(1+eng[:, 0])
    stress_true = eng[:, 1] * (1+ eng[:, 0])
    
    #print(stress_true)
 
    funcInter = interpolate.interp1d(strain_true, stress_true, bounds_error=False, fill_value = 0.0)
    
    stress_interlopated = funcInter([strain_for_interlopating])

    #curve_interlopated = np.vstack([strain_for_interlopating, stress_interlopated])
    

    strain_plastic = strain_for_interlopating - stress_interlopated / E
    
    #print(strain_plastic)
    idx = np.where(strain_plastic >= 0)

    strain_plastic = strain_plastic[idx]

    stress_plastic = stress_interlopated[idx]

    strain_plastic[0] = 0.0
    
    #print(strain_plastic)
    funcInter = interpolate.interp1d(strain_plastic, stress_plastic, bounds_error=False, fill_value=0.0)
    stress_plastic_interpolated = funcInter(strain_for_interlopating)

    idx = np.where(stress_plastic_interpolated > 0)

    strain_plastic_output = strain_for_interlopating[idx]
    stress_plastic_output = stress_plastic_interpolated[idx]

    true_curve = np.hstack([strain_plastic_output.reshape(-1,1), stress_plastic_output.reshape(-1,1)])
    true_curve[0,0] = 0.0
    #print(true_curve)
    idx = np.argmax(true_curve[:, 1])

    return true_curve[:idx,:]

def read_eng_file_to_plastic_curve(xlsx_file):
    eng_curve_dict = {}
    xlsx = pd.ExcelFile(xlsx_file)
    names = xlsx.sheet_names
    for name in names:
        df = pd.read_excel(xlsx, name)
        #df.replace('--',  0)
        eng_curve_dict[name] = df.values

    plastic_curve_dict = {}
    # if len(eng_curve_dict) == 0:
    #     return plastic_curve_dict
    #      #return None
    # else:
    if not len(eng_curve_dict) == 0:      
        for k, v in eng_curve_dict.items():
            plastic_curve_dict[k] = eng2True(v)

    return plastic_curve_dict

def read_file(xlsx_file, strain_for_interlopating):
    plastic_curve_dict = {}
    xlsx = pd.ExcelFile(xlsx_file)
    names = xlsx.sheet_names
    
    temp_dict = {}
    v_idx = []
    for name in names:
        df = pd.read_excel(xlsx, name)
        v = df.values
        temp_dict[name] = v
        v_idx.append([v[0,0], v[-1, 0]])
    
    v_idx = np.array(v_idx)
    vmin = np.max(v_idx[:, 0])
    vmax = np.min(v_idx[:, 1])

    idx = np.where(strain_for_interlopating > vmin)
    strain = strain_for_interlopating[idx]
    
    idx = np.where(strain < vmax)
    strain = strain[idx] 
    
    for k, v in temp_dict.items():
        funcInter = interpolate.interp1d(v[:, 0], v[:, 1], bounds_error=False, fill_value=0.0)
        stress_plastic_interpolated = funcInter(strain)
        idx = np.where(stress_plastic_interpolated > 0)
        v2 = np.hstack([strain[idx].reshape(-1,1), stress_plastic_interpolated[idx].reshape(-1,1)])
        plastic_curve_dict[k] = v2

    return plastic_curve_dict

def read_plastic_file_for_double_scale(xlsx_file):
    plastic_curve_dict = {}
    xlsx = pd.ExcelFile(xlsx_file)
    names = xlsx.sheet_names
    
    temp_dict = {}
    scale_dict = {}
    v_idx = []
    for name in names:
        df = pd.read_excel(xlsx, name)
        v = df.values
        #v[:, 0] /= v[-1, 0]
        #v[:, 1] /= v[-1, 1]
        temp_dict[name] = v
        v_idx.append([v[0,0], v[-1, 0]])
        scale_dict[name] = np.array([v[-1, 0], v[-1, 1]])
    
    v_idx = np.array(v_idx)
    vmin = np.max(v_idx[:, 0])
    vmax = np.min(v_idx[:, 1])

    idx = np.where(strain_for_interlopating > vmin)
    strain = strain_for_interlopating[idx]
    
    idx = np.where(strain < vmax)
    strain = strain[idx] 
    
    for k, v in temp_dict.items():
        funcInter = interpolate.interp1d(v[:, 0], v[:, 1], bounds_error=False, fill_value=0.0)
        stress_plastic_interpolated = funcInter(strain)
        idx = np.where(stress_plastic_interpolated > 0)
        v2 = np.hstack([strain[idx].reshape(-1,1), stress_plastic_interpolated[idx].reshape(-1,1)])
        plastic_curve_dict[k] = v2

    return plastic_curve_dict, scale_dict