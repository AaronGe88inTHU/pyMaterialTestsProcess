from abaqus import *
from abaqusConstants import *
import odbAccess
import numpy as np
import os

def postODB(filename, elID):
    odb = odbAccess.openOdb(filename)
    step = odb.steps['Step-1']

    triaxs = []
    eqs = []
    misess = []
    sp1s = []
    sp2s = []
    sp3s = []
    pres = []
    eleKey = ''
    for key in step.historyRegions.keys():
        if elID in key:
            eleKey = key
    element = step.historyRegions[eleKey]
    triax = element.historyOutputs['TRIAX'].data
    peeq = element.historyOutputs['PEEQ'].data
    mises = element.historyOutputs['MISES'].data
    pre = element.historyOutputs['PRESS'].data
    sp1 = element.historyOutputs['SP1'].data
    sp2 = element.historyOutputs['SP2'].data
    sp3 = element.historyOutputs['SP3'].data

    for tri, eq, mi, p, s1, s2, s3 in zip(triax, peeq, mises, pre, sp1, sp2, sp3):
        triaxs.append(tri[1])
        eqs.append(eq[1])
        misess.append(mi[1])
        pres.append(p[1])
        sp1s.append(s1[1])
        sp2s.append(s2[1])
        sp3s.append(s3[1])
        
        
    triaxs = np.array(triaxs)
    eqs = np.array(eqs)
    misess = np.array(misess)
    pres = np.array(pres)
    sp1s = np.array(sp1s)
    sp2s = np.array(sp2s)
    sp3s = np.array(sp3s)

    J3 = (sp1s + pres) * (sp2s + pres) * (sp3s + pres) #sp2s * sp2s + sp3s * sp3s - sp1s * sp2s - sp2s * sp3s - sp3s * sp1s) / 3

    J2 = (np.power(sp1s - sp2s, 2) + np.power(sp2s - sp3s, 2) + np.power(sp3s - sp1s, 2))


    #print J2
    misses2 = np.sqrt(3 * J2/6) 
    #print misses2- misess

    not0 = np.where(J3 != 0)
    J3 = J3[not0]
    misess = misess[not0]
    T = triaxs[not0]
    lode2 = T * (T * T - 1/3) * 13.5
    eqs = eqs[not0]
    
    csv = filename.split('.')[0]+'.csv'
    with open(csv,'w+') as f:
        f.write('TRIAX,LODEPS, PEEQ\n')
        for t, l, e in zip(T, lode2, eqs):
            #print(t, l, e)
            #print('%f,%f,%f\n' % (t, l, e))
            f.write('%.4f,%.4f,%.4f\n' % (t, l, e))


postODB('Job-CH4-EX.odb', '8396')