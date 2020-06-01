
# coding: utf-8

# In[1]:


#get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd
import logging
import os
import sys
from scipy import interpolate, optimize
from scipy import integrate

class LCSDGModel:

    triaxial = None
    #lodeParameter = None
    modifiedLodeParameter = None


    def __init__(self, A, n, triaxiality):
        self.triaxiality = triaxiality

    
    def triaxial2LodeParamter(self, triaxial, lodeModel):
        if self.triaxial == None:
            raise ValueError()

        else:
            self.modifiedLodeParameter = lodeModel(self.triaxial)
    

    def fitModel(self, model, tests):
        if self.triaxial == None or self.modifiedLodeParameter == None:
            raise ValueError()

        else:
            def testResult(param, tests):
                eta = test[:, 0]
                eps = model(param, tests)
                return eps

            def errfunc(param, x, y):
                return testResult(param, self.triaxial) - y

            try:
                res = optimize.least_squares(errfunc, (0.1, 1000), bounds=([0,0],np.inf), args=(tests, targets))
                with open("logging.txt",'a+') as f:
                    f.write("{0:.4f}, {1:.4f}\n".format(res.x[0], res.x[1]))
                    tt = strftime("%a, %d %b %Y %H:%M:%S +0800", gmtime())
                    f.write(tt + "\n")
            except Exception as e:
                with open("logging.txt",'a+') as f:
                    f.write(str(e))
                    tt = strftime("%a, %d %b %Y %H:%M:%S +0800", gmtime())
                    f.write(tt + "\n")
            return res

            



thetaBarPi6Model = lambda tri : np.pi / 6 - 1/3 * np.arccos(-27/ 2 * tri * (tri ** 2 - 1 / 3)) 

def errSimple(param, x, y):

def simplifiedMMC_Shell(param, eta):
    """
    Ref. Application of extended Mohr Coulomb criterion to ductile fracture Eq. 25
    output:
        epsilonPlasticFailure: failure strain
    """
    A, n, c1, c2 = param
    try:
        unit = thetaBar * np.pi / 6
    #print(param)
        comp1 = np.sqrt((1+np.power(c1, 2)) / 3) * np.cos(unit)
    #print(comp1.shape)
        comp2 = c1 * (eta + 1 / 3 * np.sin(thetaBar * unit))
    #print(A / c2 * (comp1 + comp2), -1/n)
        comp = comp1 + comp2
    #comp = comp[np.where(comp>0)]
        epsilonPlasticFailure = np.power(A / c2 * comp, -1/n)
    #print(epsilonPlasticFailure.shape)
    #print(np.any(np.isnan(epsilonPlasticFailure)))
    except(RuntimeWarning):
        
        epsilonPlasticFailure = np.zeros(comp.shape)
       
    return epsilonPlasticFailure
