import numpy as np
from scipy import interpolate
from Constants import strain_for_interlopating

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

