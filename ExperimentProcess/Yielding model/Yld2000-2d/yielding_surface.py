import numpy as np
from scipy.optimize import root
import pandas as pd
from yielding import linear_transform, principal, get_sigma

def ph_function(y, *args):
    theta, alpha, m = args
    Sigma = get_sigma(y, theta)
    L1, L2 = linear_transform(alpha)
    X1 = np.matmul(L1, Sigma[0])
    X2 = np.matmul(L2, Sigma[0])

    X11, X12 = principal(X1)
    X21, X22 = principal(X2)

    return np.power(X11 - X12, m) +\
            np.power(np.abs(2 * X22 + X21), m) + \
            np.power(np.abs(2 * X21 + X22), m) - 2

alpha = np.array([0.88159522, 0.9972777,\
                0.78543291, 1.01720254,\
                1.03660762, 0.99413679,\
                1.01201587, 1.21529707])

#for theta in np.arange(0, np.pi/2, np.pi/16):
xxs = []
yys = []
for theta in np.arange(0, 9 * np.pi/16, np.pi/16):
    sig = root(ph_function, 1, (theta, alpha, 8))
    xx, yy, xy =  get_sigma(sig.x, theta)[0]
    xxs.append(xx)
    yys.append(yy)

df_d2f = pd.DataFrame(np.hstack([xxs,yys]).reshape(-1,2), columns = ['xx','yy'])
df_d2f.to_excel('surface.xlsx')