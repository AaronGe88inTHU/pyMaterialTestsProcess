
# coding: utf-8

# In[4]:

import sys
import numpy as np
from scipy.optimize import curve_fit
from ReadFile import readTestInfo, readElastic
from matplotlib import pyplot as plt
import pandas as pd


# In[5]:


def ElasticParameter(fileName, width, thick, bound = None):
    e1 = readTestInfo(fileName, 'strainE.csv', 'e1')
    e2 = readTestInfo(fileName, 'strainE.csv', 'e2')

    force = e1[:, 2]

    sigEng = force / width / thick

    eEng = e1[:,1]
    e2Eng = e2[:, 1]
    plt.plot(eEng, sigEng)
    

    def linear_curve (x, a, b):
        return a * x + b
    
    Emod = 0

    if not bound == None:
        lb, ub = bound

        elasticL = sigEng > lb
        elasticU = sigEng < ub

        elastic = elasticU & elasticL
        eElastic = eEng[elastic]

        sigElastic = sigEng[elastic]

        popt, _ = curve_fit(linear_curve, eElastic, sigElastic)
        Emod = popt[0]
        plt.plot(eElastic, linear_curve(eElastic, *popt), 'r--')

        df = pd.DataFrame(np.hstack([eEng.reshape(-1, 1), e2Eng.reshape(-1, 1), sigEng.reshape(-1, 1)]), columns=['e1', 'e2', 'sig'])
        df.to_excel('Eng.xlsx')
    
    plt.show()
    return Emod
        
def hardenParamter(EMod = 207000, poi = 0.28, ep0 = 1.67e-2, uncompression = True):
    #e1 = readTestInfo(fileName, 'strain.csv', 'e1')
    #e2 = readTestInfo(fileName, 'strain.csv', 'e2')
    e1
    eng = readElastic('Eng.xlsx')
    e1, sig, rate = eng[:, 0], eng[:, 1], eng[:, 2]
    
    e1T = np.log(1 + e1)


    sigT = sig * (1 + e1)

    #e1P = e1 - sig / EMod

    plastic = (e1 - sig/EMod) > 0.002



    e1TP = (e1T - sigT / EMod)[plastic]
    sigTP = sigT[plastic]

    ub = np.argmax(sigTP)

    e1UB = e1TP[0:ub]
    sigUB = sigTP[0:ub]
    
    def Johnson_Cook(x, A, B, n, m):
        """
        x[0]: plastic epsilon 
        x[1]: rate of plastic epsilon
        """
        return A + B * x[0]

    def VoceLaw(x, k0, Q, B):
        return k0 + Q * (1 - np.exp(-B * x))

    

    
    optSwift, _ = curve_fit(SwiftLaw, e1UB, sigUB, p0=[1000, 0.01, 0.2], bounds=(0, [100000, 0.5, 1]))
    optVoce, _ = curve_fit(VoceLaw, e1UB, sigUB, p0=[200, 300, 10])
    optSwift

    def MixedLaw(x, w):
        return w * SwiftLaw(x, *optSwift) + (1-w) * VoceLaw(x, *optVoce)

    optMixed, _ = curve_fit(MixedLaw, e1UB,sigUB, p0=0.5, bounds=(0,1))

    print(optSwift, optVoce, optMixed)
    #sig = trueStrain(e1[:, 2], e1[:, 1], width, thick)
    #result = np.hstack([e1[:,1].reshape(-1,1), e2[:,1].reshape(-1,1), sig.reshape(-1,1)])
    plt.plot(e1TP, sigTP, label = 'True stress - strain curve')
    plt.plot(e1UB, sigUB,'r--', label = 'Before fracture initation')
    #plt.plot(e1UB, SwiftLaw(e1UB, *optSwift), 'g*', label = 'Swift law')
    #plt.plot(e1UB, VoceLaw(e1UB, *optVoce), 'b^', label = 'Voce law')
    z2e = np.arange(0, e1UB[-1], 0.004)
    sigz2e = np.interp(z2e, e1UB, sigUB)
    e2o = np.arange(e1UB[-1], 1, 0.004)
    sige2o = MixedLaw(e2o, *optMixed)
    #sige2o[0] = sigUB[0]

    z2o = np.hstack([z2e, e2o])
    z2o[0] = 0
    sigz2o = np.hstack([sigz2e, sige2o])
    plt.plot(e2o, sige2o, 'y-', label = 'Mixed law Extraplation')
    plt.xlabel('True Strain')
    plt.ylabel('Stress')
    plt.legend()
    plt.show()

    e1TP[0] = 0
    e2TP[0] = 0
    if uncompression:
        e3TP = 0 - e1TP - e2TP
    else:
        e3TP = np.zeros(e1TP.shape)
    
    df1 = pd.DataFrame(np.hstack([e1TP.reshape(-1, 1), e2TP.reshape(-1, 1),e3TP.reshape(-1,1), sigTP.reshape(-1,1)]), columns = ['e1', 'e2', 'e3', 'sig'])

    #df = pd.DataFrame(result, columns=['e1','e2', 'sig'])
    df1.to_excel('Plastic.xlsx','1')
    df2 = pd.DataFrame(np.hstack([z2o.reshape(-1,1), sigz2o.reshape(-1,1)]), columns = ['ep','sig'])
    df2.to_csv('harden.csv', float_format='%.5f', header=False, index= False)

    

def main(argv):
    if argv == None:
        print('world~!')
    else:
        print(argv)
        fileName, width, thick, direction = argv[1:5]
        lb, up = argv[5:7]
        #Emod = ElasticParameter(fileName, float(width), float(thick), [float(lb), float(up)])
        #print(Emod)

        hardenParamter(205000, 0.28)
        #strainStressU(fileName, float(width), float(thick))
        #strokeForce(fileName, direction)
        
if __name__=="__main__":
    main(sys.argv)
    



# In[21]:





# In[16]:





# In[20]:





# In[23]:




