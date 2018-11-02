import numpy as np
from scipy.linalg import solve


#def uniTension(Young, strain, stress):
#    plasticStrain = 
#    return 

def uniTension(sigmaYield, poison):
    I1 = sigmaYield
    J2 = np.power(I1, 2) / 3
    return I1, J2

def buttTension(sigmaYield, poison):
    I1 = (1+poison)/(1-poison) * sigmaYield
    J2 = np.power((1 - 2 * poison)/(1 + poison), 2) / 3 * np.power(I1, 2)
    return I1, J2

def yieldingSurface(func, sigmaYield, poison, tau_0):
    I1, J2 = func(sigmaYield, poison)
    a = tau_0 * I1 / np.sqrt(3)
    b = np.power(I1, 2) / 3
    c = np.power(tau_0, 2) - J2
    return a, b, c

elasticPoison = 0.385
tau0 = 11.3
a1, b1, c1 = yieldingSurface(uniTension, 17.3, elasticPoison, tau0)
a2, b2, c2 = yieldingSurface(buttTension, 25, elasticPoison, tau0)
a = np.array([[a1, b1], 
            [a2, b2]])
print(a1, b1, c1)
print(a2, b2, c2)
b = np.array([c1, c2])

x = solve(a, b)

print(x)