import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

def UniTension(table, bound, unCompression=True):
    lo, up = bound
    e1 = table[:, 0]
    e2 = table[:, 1]
    sig = table[:, 2]
    
    e1 = e1[np.where(~np.isnan(e1))]
    e2 = e2[np.where(~np.isnan(e2))]
    sig = sig[np.where(~np.isnan(sig))]

    elastic = np.where(sig < up)

    e1Elastic = e1[elastic]
    e2Elastic = e2[elastic]
    sigElastic = sig[elastic]

    

    elastic = np.where(sigElastic > lo)

   

    e1Elastic = e1Elastic[elastic]
    e2Elastic = e2Elastic[elastic]
    sigElastic = sigElastic[elastic]

    def linear(x, a, b):
        return a + b * x
    
    young, _ = curve_fit(linear, e1Elastic, sigElastic)
    poisson, _ = curve_fit(linear, e1Elastic, e2Elastic)

    
    e1Plastic = e1 - sig/ young[1]
    e2Plastic = e2 - poisson[1] / young[1] * sig

    plastic = np.where(e1Plastic >= 0.002)

    e1Plastic = e1Plastic[plastic]
    e2Plastic = e2Plastic[plastic]

    sigPlastic = sig[plastic]

    if unCompression:
        e3Plastic = 0 - e1Plastic - e2Plastic
    else:
        e3Plastic = np.zeros(e1Plastic.shape)

    youngOne = young[1] * np.ones(e1Plastic.shape)
    poissonOne = poisson[1] * np.ones(e1Plastic.shape) 
    #res = np.hstack([])
    res = np.vstack([youngOne, poissonOne, e1Plastic, e2Plastic, e3Plastic, sigPlastic])
    dfRes = pd.DataFrame(res.T, columns=['Young', 'Poisson', 'e1p', 'e2p', 'e3p', 'sig'])
    dfRes.to_excel('Uniten.xlsx', sheet_name='sheet1')
    return 

df = pd.read_excel('harden.xlsx')
table = df.values
UniTension(table, (10, 130), True)