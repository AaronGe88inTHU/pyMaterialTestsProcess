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
    c = tau_0 ** 2 - J2
    return a, b, c

def yieldingSurface2(tau0, a1, a2):
    #I, J2 = func()
    pass


elasticPoison = 0.377
tau0 = 19.1
uni = 21.7
res = []
print(uniTension(uni,elasticPoison)[0], np.sqrt(uniTension(uni,elasticPoison)[1]))
for butt in np.arange(10, 16, 1):
#    for uni in np.arange(22, 28, 0.5):
    a1, b1, c1 = yieldingSurface(uniTension, uni, elasticPoison, tau0)
    a2, b2, c2 = yieldingSurface(buttTension, butt, elasticPoison, tau0)
    a = np.array([[a1, b1], 
                    [a2, b2]])
    b = np.array([c1, c2])
    x = solve(a, b)
    if x[0] > 0 and x[1] > 0:
        al1 = x[0]
        al2 = x[1]
        p1 = al2 / 3
        p2 = 1/np.sqrt(3)*al1*tau0
        print('butt', butt)
        print(np.sqrt((tau0**2+(p2/2/p1)**2)/p1))
        print(p2/2/p1)
        print(x, buttTension(butt,elasticPoison)[0], np.sqrt(buttTension(butt,elasticPoison)[1]))
        print('**********')

