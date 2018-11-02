import numpy as np
from GISSIMO import simplifiedMMC, accumulatedDamage
from scipy import optimize
import Paramters

def testResults(tests, param):
    """
    tests result to damgaIndicator
    """
    indicators = np.zeros([tests.shape[0]])
    for ii, test in enumerate(tests):
        eta = test[:, 0]
        theta = test[:, 1]
        epsilon = test[:, 2]
        damageIndicator = accumulatedDamage(simplifiedMMC, eta, theta, epsilon, param)
        indicators[ii] = damageIndicator
    return indicators

def func(param, x):
    return testResults(x, param)
    

def err(param, x, y):
    c1, c2 = param
    #print(Paramters.A, Paramters.n)
    return func((Paramters.A, Paramters.n, c1, c2), x) - y

def fitModel(tests):
    targets = np.ones([tests.shape[0]])
    res = optimize.leastsq(err, (0.1, 500), (tests, targets))
    #print(err(res[0], tests, targets))
    return res[0]
