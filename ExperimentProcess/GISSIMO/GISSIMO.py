import numpy as np
from scipy import integrate


def simplifiedMMC(eta, thetaBar, param):
    """
    simplified MMC model 
    sigma = A * eps_p^n
    output:
        epsilonPlasticFailure: failure strain
    """
    A, n, c1, c2 = param
    print(param)
    comp1 = np.sqrt((1+np.power(c1, 2)) / 3) * np.cos(thetaBar * np.pi / 6)
    comp2 = c1 * (eta + 1 / 3 * np.sin(thetaBar * np.pi / 6))
    epsilonPlasticFailure = np.power(A / c2 * (comp1 + comp2), -1/n)

    return epsilonPlasticFailure

def accumulatedDamage(model, eta, thetaBar, epsilon, param):
    """
    Accumulating Damage Model
    input:
        model: Damage model
        eta: eta list
        thetaBar: theraBar list
        epsilon: epsilon List
        param: A, n, c1, c2
    output:
        damage Indicator
    """
    #'epsilonMMC = np.zeros(eta.shape)'
    #'for ii, (eta, thetaBar) in  enumerate(zip(eta, thetaBar)):'
    epsilonPlaticFailure = model(eta, thetaBar, param)
    #'epsilonMMC[ii] = epsilonPlaticFailure'
    
    damageIndicator = integrate.simps(1 / epsilonPlaticFailure, epsilon)

    return damageIndicator

def MMCSurface(*param):
    eta = np.arange(-1, 1.1, 0.1)
    theta = np.arange(-1, 1.1, 0.1)
    etaX, thetaY = np.meshgrid(eta, theta, sparse=False)
    #z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
    #h = plt.contourf(x,y,z)
    epsilon = simplifiedMMC(etaX, thetaY, param)
    return etaX, thetaY, epsilon
    