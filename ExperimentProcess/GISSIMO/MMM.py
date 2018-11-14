
#%%
import numpy as np
import pandas as pd
import logging
import os
from scipy import interpolate


#%%
def preProcess(cwd):
    fileNames = os.listdir(cwd)
    clearedData = pd.ExcelWriter('clearedData.xlsx')
    for f in fileNames:
        if f.startswith('~$'):
            continue
        print(f)
        if os.path.splitext(f)[1] == '.xlsx':
            ff = os.path.join('data', f)
            df = pd.read_excel(ff, 'Sheet1')
            time = df.loc[:,'TIME'].values[1:]
            time1 = df.loc[:, 'TIME.1'].values[1:]
            
            time = np.array(time)[~np.isnan(time)]
            time1 = np.array(time1)[~np.isnan(time1)]
            
            (timeEps, timeLP) = (time, time1) if len(time) < len(time1) else (time1, time)
            eps = df.loc[:, 'EPS'].values[1:]
            eps = np.array(eps)[~np.isnan(eps)]
            
            #timeLP = np.array(timeLP)[np.where(timeLP < np.max(timeEps))]
            #wprint(timeLP)
            timeLP = timeLP[timeLP < np.max(timeEps)]
            
            funcInterp = interpolate.interp1d(timeEps, eps, bounds_error=None)
            try:
                epsFullLength = funcInterp(timeLP).reshape(-1,1)
            except(ValueError):
                print(timeLP, timeEps)
            
            timeLP = timeLP.reshape(-1,1)
            LP = df.loc[:,'LP'].values[1:]
            LP = LP[0:len(timeLP)].reshape(-1,1)
            
            TRI = df.loc[:,'TRI'].values[1:]
            TRI = TRI[0:len(timeLP)].reshape(-1, 1)

            data = np.hstack([timeLP, epsFullLength, LP, TRI])
            dff = pd.DataFrame(data, columns=['TIME', 'EPS', 'LP', 'TRI'])
            dff.to_excel(clearedData, sheet_name=os.path.splitext(f)[0])
    clearedData.save()


#%%
preProcess('/Users/aaron/Documents/GitHub/pyMaterialTestsProcess/ExperimentProcess/GISSIMO/data')


#%%
def readXlsx(fileName):
    """
    read all sheets in xls file
    input:
        fileName
    output:
        listEta, listThetaBar, listEpsilon in sheets
    """
    xlsx = pd.ExcelFile(fileName)
    etaThetaEpsilon = []
    for sheet in xlsx.sheet_names:
        #print(sheet)
        df = pd.read_excel(xlsx, sheet)
        eta = df.loc[:, 'TRI'].values.reshape(-1, 1)
        thetaBar = df.loc[:, 'LP'].values.reshape(-1, 1)
        eplison = df.loc[:, 'EPS'].values.reshape(-1, 1)
        ind = np.where(eplison>0)
        #print(sheet)
        #print(ind)
        ete = np.hstack([eta, thetaBar, eplison])
        
        etaThetaEpsilon.append(ete[ind[0],:])
    
    #logging.debug(etaThetaEpsilon)
    etaThetaEpsilon = np.array(etaThetaEpsilon)
    return etaThetaEpsilon


#%%
tests = readXlsx('clearedData.xlsx')


#%%
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

fig = plt.figure()

ax = fig.gca(projection='3d')
for test in tests:
    xx, yy, zz = test[:, 0], test[:, 1], test[:, 2]
    ax.plot(xx, yy, zz)#, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    ax.xaxis.set_major_locator(LinearLocator(5))
    ax.yaxis.set_major_locator(LinearLocator(5))
    ax.set_xlabel('Triaxiality')
    ax.set_ylabel('Lode Parameter')
    ax.set_zlabel('Failure plastic strain')

plt.show()


#%%
from scipy import integrate

def simplifiedMMC(eta, thetaBar, param):
    """
    simplified MMC model 
    sigma = A * eps_p^n
    output:
        epsilonPlasticFailure: failure strain
    """
    A, n, c1, c2 = param
    #print(param)
    comp1 = np.sqrt((1+np.power(c1, 2)) / 3) * np.cos(thetaBar * np.pi / 6)
    #print(comp1.shape)
    comp2 = c1 * (eta + 1 / 3 * np.sin(thetaBar * np.pi / 6))
    #print(A / c2 * (comp1 + comp2), -1/n)
    comp = comp1 + comp2
    #comp = comp[np.where(comp>0)]
    epsilonPlasticFailure = np.power(A / c2 * comp, -1/n)
    #print(epsilonPlasticFailure.shape)
    #print(np.any(np.isnan(epsilonPlasticFailure)))
    return epsilonPlasticFailure

def accumulatedDamage(model, eta, thetaBar, epsilon, param):
    """
    Accumulating Damage Model
    input:
        model: Damage mode
        eta: eta list
        thetaBar: theraBar list
        epsilon: epsilon List
        param: A, n, c1, c2
    output:
        damage Indicator
    """
    #'epsilonMMC = np.zeros(eta.shape)'
    #'for ii, (eta, thetaBar) in  enumerate(zip(eta, thetaBar)):'
    epsilonPlasticFailure = model(eta, thetaBar, param)
    #'epsilonMMC[ii] = epsilonPlaticFailure'
   
    damageIndicator = integrate.trapz(1/ epsilonPlasticFailure, epsilon)
                      #np.sum(epsilon / epsilonPlasticFailure)
                      #integrate.tr (1 / epsilonPlaticFailure, epsilon)

    #print(epsilonPlasticFailure)
    return damageIndicator

def MMCSurface(*param):
    eta = np.arange(0, 1.1, 0.1)
    theta = np.arange(-1, 1.1, 0.1)
    etaX, thetaY = np.meshgrid(eta, theta, sparse=False)
    #z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
    #h = plt.contourf(x,y,z)
    epsilon = simplifiedMMC(etaX, thetaY, param)
    return etaX, thetaY, epsilon


#%%
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
    return (epsMMC - epsTest).T[0]

def fitModelUsingFractureStrain(tests):
    targets = np.ones([tests.shape[0]])
    #result = testResults(tests,(996.68, 0.026, 0.1, 500))
    res = optimize.least_squares(errFractureStrain, (500, 0.1, .1, 600), args=(tests, targets))
    
    #print(err(res[0], tests, targets))
    #indicators = testResults(tests, (96.68, 0.02772, res[0][0], res[0][1]))
    #Aprint(func((996.68, 0.02772,res[0][0], res[0][1]), tests))
    return res

def fitDamageAcc(tests, res0):
    targets = np.ones([tests.shape[0]])
    #result = testResults(tests,(996.68, 0.026, 0.1, 500))
    res = optimize.least_squares(errAcc, res0, args=(tests, targets))
    
    #print(err(res[0], tests, targets))
    #indicators = testResults(tests, (96.68, 0.02772, res[0][0], res[0][1]))
    #Aprint(func((996.68, 0.02772,res[0][0], res[0][1]), tests))
    return res


#%%
resUsingFractureStrain = fitModelUsingFractureStrain(tests)
resUsingFractureStrain


#%%
resAcc = fitDamageAcc(tests, resUsingFractureStrain.x)
resAcc


#%%
def planeStressMMC(model, param):
    points = []
    for sigma1 in np.range(0, 1.1, 0.1):
        sigma2 = 0
        while True:
            pressure = (sigma2 + sigma1) / 3
            mises = np.sqrt(((sigma1-sigma2) ** 2 + sigma2 ** 2 + sigma1 ** 2)/2)
            tri = pressure / mises
            lp = (2 * sigma2 - sigma1) / sigma1
            points.append(tri, lp)
            sigma2 = sigma2 + 0.1
            if(sigma2 > sigma1):
                break
    triLp = np.array(points)
    strain = model(triLp[:, 0], triLp[:, 1], param)
    
    return np.hstack([triLp, strain]).reshape(-1,1) 
line = planeStressMMC(simplifiedMMC, resAcc)

def showFigure(faiureSurface, tests):
    XX, YY, zz = faiureSurface
    fig = plt.figure()
    #plt.xlabel('Triaxiality')
    #plt.ylabel('Lode Parameter')
    #plt.zlabel('Failure plastic strain')
    ax = fig.gca(projection='3d')
    #cs = ax.contourf(X, Y, z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)
    #cbar = fig.colorbar(cs)
    ax.scatter3D(XX, YY, zz, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
    for test in tests:
        xx, yy, zz = test[:, 0], test[:, 1], test[:, 2]
        ax.plot(xx, yy, zz)#, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    global line
    ax.plot(line[:, 0], )
    ax.xaxis.set_major_locator(LinearLocator(5))
    ax.yaxis.set_major_locator(LinearLocator(5))
    ax.set_xlabel('Triaxiality')
    ax.set_ylabel('Lode Parameter')
    ax.set_zlabel('Failure plastic strain')
    ax.set_zbound([0,1.5])
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f')
    plt.show()


#%%
a, b , c, d = resAcc.x[:]
failureSurface = MMCSurface(a, b, c,d)
showFigure(failureSurface, tests)


#%%



