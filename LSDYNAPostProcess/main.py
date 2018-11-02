import sys
#from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict
import pandas as pd
from eloutReader import eloutReader, effectStrain
from kReader import setLoader



def gauge(elementSet, elout):
    gaugeHistory = defaultdict(list)
    for idSet, elSet in elementSet.items():
        found = []
        for idEle, strainHistory in elout.items():
            if idEle in elSet[0]:
                #eleHistory = [effectStrain(ll) for ll in strainHistory]
                eleHistory = [ll[0] for ll in strainHistory]
                gaugeHistory[idSet].append(eleHistory)
                found.append(idEle)
        [elout.pop(ll) for ll in found]
    return gaugeHistory

def main(argv):
    kName = argv[1]
    ele = setLoader(kName)
    elout = eloutReader('elout')
    #lst = elout[1424]
    #print(len(lst[0]))
    #history = [effectStrain(ll) for ll in lst] 
    #plt.plot(history)
    #plt.show()
    history = gauge(ele, elout)

    columns = []

    gaugeData = []
    for k, v in history.items():
        #print(k, v)
        aver = np.average(np.array(v), axis=0)
        #print(aver.shape)
        #plt.plot(aver)
        columns.append(str(k)[1:])
        gaugeData.append(aver)
    #plt.show()
    gaugeData = np.array(gaugeData).reshape(-1, len(columns))
    df = pd.DataFrame(gaugeData, columns = columns)
    df.to_excel('gauge.xlsx','1')

if __name__ == "__main__":
    main(sys.argv)