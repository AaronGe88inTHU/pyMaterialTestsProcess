
# coding: utf-8

# In[4]:

import sys
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import pandas as pd
import os

# In[5]:


def strokeForce(machine, fileName, cameraName, direction, guage):
    #up = readTestInfo(fileName, 'up.csv', direction)
    if machine == "WB":
        from ReadFile_WB import readTestInfo, readElastic
    elif machine == "Z100":
        from ReadFile_Z100 import readTestInfo, readElastic
    elif machine == "H050":
        from  ReadFile_H050 import readTestInfo, readElastic
    elif machine == "H050_T":
        from ReadFile_H050_T import readElastic, readTestInfo
    else:
        from ReadFile import readElastic, readTestInfo
    E = readTestInfo(fileName, 'E.csv', 'E', cameraName)
    stroke =  E[:, 1] * guage
    #print(stroke)
    result = np.hstack([stroke.reshape(-1,1), E[:,-1].reshape(-1,1)])
    plt.plot(result[:,0], result[:,1])
    plt.show()
    df = pd.DataFrame(result, columns=['stroke', 'force'])
    df.to_excel('sf.xlsx','1')


def ElasticParameter(machine,fileName, cameraName, width, thick, bound = None):
    if machine == "WB":
        from ReadFile_WB import readTestInfo, readElastic
    elif machine == "Z100":
        from ReadFile_Z100 import readTestInfo, readElastic
    elif machine == "H050":
        from  ReadFile_H050 import readTestInfo, readElastic
    elif machine == "H050_T":
        from ReadFile_H050_T import readElastic, readTestInfo
    else:
        from ReadFile import readElastic, readTestInfo
    e1 = readTestInfo(fileName, 'strain.csv', 'e1', cameraName)
    e2 = readTestInfo(fileName, 'strain.csv', 'e2', cameraName)
    
    print(e1, e2)
    force = e1[:, 2]

    sigEng = force / width / thick

    eEng = np.exp(e1[:,1]) - 1 
    e2Eng = np.exp(e2[:, 1]) - 1
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
        e2Elastic = e2Eng[elastic]
        sigElastic = sigEng[elastic]

        popt, _ = curve_fit(linear_curve, eElastic, sigElastic)
        Emod = popt[0]
        
        popt, _ = curve_fit(linear_curve, eElastic, e2Elastic)
        poison = - popt[0]

        plt.plot(eElastic, linear_curve(eElastic, *popt), 'r--')

        df = pd.DataFrame(np.hstack([eEng.reshape(-1, 1), sigEng.reshape(-1, 1)]), columns=['e1',  'sig'])
        df.to_excel('Eng.xlsx')
    
    plt.show()
    return Emod, poison
        
def hardenParamter(machine, fileName, cameraName, EMod = 207000, poi = 0.28, uncompression = True):
    if machine == "WB":
        from ReadFile_WB import readTestInfo, readElastic
    elif machine == "Z100":
        from ReadFile_Z100 import readTestInfo, readElastic
    elif machine == "H050":
        from  ReadFile_H050 import readTestInfo, readElastic
    elif machine == "H050_T":
        from ReadFile_H050_T import readElastic, readTestInfo
    else:
        from ReadFile import readElastic, readTestInfo
    e1T = readTestInfo(fileName, 'strain.csv', 'e1', cameraName)[:,1]
    e2T = readTestInfo(fileName, 'strain.csv', 'e2', cameraName)[:,1]
    
    #print(e1T)
    
    eng = readElastic('Eng.xlsx')
    
    #print(eng.shape)
    sig  =  eng[:, -1]
    
    #print(sig)
    
    nan_index = np.isnan(e1T)

    #n_index = np.argwhere([not x for x in nan_index])
    #e1T = e1T[n_index]
    #e2T = e2T[n_index]
    
    if uncompression:
        e3T = 0 - e1T - e2T
    else:
        e3T = np.zeros(e1T.shape)

    vm = np.sqrt(2) / 3 * np.sqrt((e1T - e2T) ** 2 + (e2T- e3T) ** 2 + (e3T - e1T) ** 2)
    #df = pd.DataFrame(vm)
    #df.to_csv('vm.csv')
    
    sigT = sig * np.exp(e1T)
    
    #e1P = e1 - sig / EMod
    #print(e1T.shape, sigT.shape)
    plastic = (e1T - sig/EMod) > 0.002
   
    #print(plastic.shape)
    e1TP = (e1T - sigT / EMod)[plastic]
    e2TP = (e2T + poi * sigT / EMod)[plastic]
    sigTP = sigT[plastic]
    

    #print(e1TP.shape, sigTP.shape)
    
    df = pd.DataFrame(np.hstack([e1TP.reshape(-1,1), sigTP.reshape(-1,1)]))
    #df.to_csv('pc.csv')
    
    ub = np.argmax(sigTP)

    e1UB = e1TP[0:ub]
    #e2UB = e2TP[0:ub]
    sigUB = sigTP[0:ub]
    
    def SwiftLaw(x, A, e0, n):
        return A * (x + e0) ** n

    def VoceLaw(x, k0, Q, B):
        return k0 + Q * (1 - np.exp(-B * x))

    

    
    optSwift, _ = curve_fit(SwiftLaw, e1UB, sigUB, p0=[1000, 0.01, 0.2], bounds=(0, [100000, 0.5, 1]))
    print(optSwift)
    optVoce, _ = curve_fit(VoceLaw, e1UB, sigUB, p0=[200, 300, 10])
    

    def MixedLaw(x, w):
        return w * SwiftLaw(x, *optSwift) + (1-w) * VoceLaw(x, *optVoce)

    optMixed, _ = curve_fit(MixedLaw, e1UB,sigUB, p0=0.5, bounds=(0,1))

    #print(optSwift, optVoce, optMixed)
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
        os.chdir("//Volumes//GE-KINGSTON//CH//CH-1")
        #files = os.listdir(os.getcwd())
        import glob
        f = glob.glob("*.xlsx")
        #print(f)

        machine, fileName, cameraName, width, thick, direction = argv[0:6]
        lb, up = argv[6:8]
        #Emod, poison = ElasticParameter(machine, f[0], cameraName, float(width), float(thick), [float(lb), float(up)])
        #print(Emod, poison)

        #hardenParamter(machine, fileName, cameraName, 165000, 0.38)
        #strainStressU(fileName, float(width), float(thick))
        strokeForce(machine, fileName, cameraName, direction, 10)
        
if __name__=="__main__":
    main(["WB", "CH-1.xlsx", "0.06mmpmin-1.csv", "5", "2", "E", "50", "300"])
    
    






