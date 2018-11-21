import numpy as np
from scipy.linalg import solve


#def uniTension(Young, strain, stress):
#    plasticStrain = 
#    return 

def uniTension(sigmaYield, poison):
    """
    sigma 1 = sy
    sigma2 = 0
    sigma3 = 0
    """
    I1 = sigmaYield
    J2 = np.power(I1, 2) / 3
    return I1, J2

def buttTension(sigmaYield, poison):
    """
    sigma1 = 　
    """
    I1 = (1+poison)/(1-poison) * sigmaYield
    J2 = np.power((1 - 2 * poison)/(1 + poison), 2) / 3 * np.power(I1, 2)
    return I1, J2

def yieldingSurface(func, sigmaYield, poison, tau_0):
    I1, J2 = func(sigmaYield, poison)
    a = tau_0 * I1 / np.sqrt(3)
    b = np.power(I1, 2) / 3
    c = np.power(tau_0, 2) - J2
    return a, b, c

def yieldingSurface2(tau0, a1, a2):
    #I, J2 = func()
    pass


elasticPoison = 0.399
tau0 = 23.7

res = []
for butt in np.arange(15, 30, 0.5):
    for uni in np.arange(22, 28, 0.5):
        a1, b1, c1 = yieldingSurface(uniTension, uni, elasticPoison, tau0)
        a2, b2, c2 = yieldingSurface(buttTension, butt, elasticPoison, tau0)
        a = np.array([[a1, b1], 
                    [a2, b2]])
        b = np.array([c1, c2])
        x = solve(a, b)
        if x[1] > 0 and x[0] > 0:
            res.append([uni, butt, x])
print(res)