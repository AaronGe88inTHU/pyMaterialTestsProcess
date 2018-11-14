import numpy as np
from GISSIMO import simplifiedMMC, accumulatedDamage
from scipy import optimize

def testResultsAcc(param, tests):
    """
    tests result to damgaIndicator
    """
    indicators = np.zeros([tests.shape[0]])
    for ii, test in enumerate(tests):
        eta = test[:, 0]
        theta = test[:, 1]
        epsilon = test[:, 2]
        damageIndicator = accumulatedDamage(simplifiedMMC, eta, theta, epsilon, param)
        #print(damageIndicator)
        indicators[ii] = damageIndicator
    return indicators

def testResulsUsingFractureStrain(param, tests):
    epsMMC = np.array([simplifiedMMC(test[-1,0], test[-1, 1], param) for test in tests]).reshape(-1,1)
    #epsTest = tests[:, -1, 2].reshape(-1,1)
    return epsMMC 

def errAcc(param, x, y):
    A, n, c1, c2 = param
    #print(Paramters.A, Paramters.n)
    return testResultsAcc((A,n, c1, c2), x) - y

def errFractureStrain(param, x, y):
    epsMMC = testResulsUsingFractureStrain(param, x)
    epsTest = np.array([test[-1, 2] for test in x]).reshape(-1,1)
    #print((epsMMC-epsTest).T)
    #print(epsMMC-epsTest.T[0])
    return (epsMMC - epsTest).T[0] 
    #return np.sum((epsMMC - epsTest).T[0] ** 2)

def fitModelUsingFractureStrain(tests):
    targets = np.ones([tests.shape[0]])
    #result = testResults(tests,(996.68, 0.026, 0.1, 500))
    #res = optimize.differential_evolution(errFractureStrain,bounds=([0,5000],[0,100],[0, 100],[0, 10000]), args=(tests, targets))
    #res0 = (2000, 0.1, .1, 6000)
    res = optimize.least_squares(errFractureStrain, x0=(2000, 0.1, .1, 6000), bounds=([0,0,0,0],[10000, 100,1000,10000]), args=(tests, targets))
    #print(err(res[0], tests, targets))
    #indicators = testResults(tests, (96.68, 0.02772, res[0][0], res[0][1]))
    #Aprint(func((996.68, 0.02772,res[0][0], res[0][1]), tests))
    return res

def fitDamageAcc(tests, res0):
    targets = np.ones([tests.shape[0]])
    #result = testResults(tests,(996.68, 0.026, 0.1, 500))
    res = optimize.least_squares(errAcc, res0, bounds=([0,0,0,0],[10000, 100,1000,10000]), args=(tests, targets))
    
    #print(err(res[0], tests, targets))
    #indicators = testResults(tests, (96.68, 0.02772, res[0][0], res[0][1]))
    #Aprint(func((996.68, 0.02772,res[0][0], res[0][1]), tests))
    return res
