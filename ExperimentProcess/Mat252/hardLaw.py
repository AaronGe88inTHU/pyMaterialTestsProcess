import numpy as np

def TAPOHardLaw(r, tau0, q, b, H):
    sigma = tau0 + q * (1 - np.exp(-b * r)) +  H * r
    return sigma

r = np.arange(0, 0.2, 0.01)
tau0 = np.average([22.3, 24.88, 23.92])
q = np.average([7.76, 6.19, 6.23])
b = np.average([40.59, 49.48, 47.46])
H = np.average([8.11, 6.82, 13.58])

stress = TAPOHardLaw(r, tau0, q, b, H)

import pandas as pd
df = pd.DataFrame(np.vstack([r, stress]), ['r', 'sigma'])
df.to_csv('hard.csv')
