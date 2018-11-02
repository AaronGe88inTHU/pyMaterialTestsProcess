import sys
from matplotlib import pyplot as plt
import numpy as np
from collections import defaultdict

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
    ele = setLoader('cone_s_withset_2.k')
    elout = eloutReader('elout')
    #lst = elout[1424]
    #print(len(lst[0]))
    #history = [effectStrain(ll) for ll in lst] 
    #plt.plot(history)
    #plt.show()
    history = gauge(ele, elout)
    for k, v in history.items():
        #print(k, v)
        aver = np.average(np.array(v), axis=0)
        #print(aver.shape)
        plt.plot(aver)
    plt.show()
if __name__ == "__main__":
    main(sys.argv)