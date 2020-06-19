#!/usr/bin/env python
# coding: utf-8
import sys
import numpy as np
c1 = float('<<c1>>')
c2 = float('<<c2>>')
A = float('<<A>>')
n = float('<<n>>')

aa = float('<<aa>>')
bb = float('<<bb>>')


# c1 = 0.12
# c2 = 720
# A = 1276
# n = 0.2655

# aa = 1
# bb = 0.1

"""
Wierzbicki and XUe (2005)
relation of triax and lodep
"""
lode_p = lambda triax: -27 / 2 * triax * (np.power(triax, 2) - 1/3)

"""
Y. Bai, T. Wierzbicki (2008)
relation of lodep and lodeb
"""
lode_b = lambda lodep: 1 - 2/np.pi * np.arccos(lodep)

def eps_i(triax):
    """
    LS-DYNA manual
    instablity curve
    """ 
    global aa, bb
    output = aa * np.power(triax - 0.33, 2) + bb
    return output

def eps_f(triax, lodeb):
    """
    Y. Bai, T. Wierzbicki (2008)
    Simplified MMC model
    """ 
    global c1, c2, A, n
    
    term_1 = np.sqrt((1 + np.power(c1, 2)/ 3)) * np.cos(lodeb * np.pi / 6)
    #print(term_1)
    term_2 = c1 * (triax + np.sin(lodeb * np.pi / 6)/3)
    #print(term_2)
    eps = np.power(A/c2*(term_1+term_2), -1/n)
    #print(eps)
    return eps

#def 

def writeSDGCurve(triax, eps):
    #print(param)
    with open('5000.cur', 'w+') as f:
        f.write('*KEYWORD\n')
        f.write('*DEFINE_CURVE'+'\n')
        f.write('$#Triaxiality vs. Failure Plastic Strain'+'\n')
        f.write('$'+'{:>9}'.format('LCID')+
                '{:>10}'.format('SIDR') + 
                '{:>10}'.format('SCLA') + 
                '{:>10}'.format('SCLO') + 
                '{:>10}'.format('OFFA') +
                '{:>10}'.format('OFFO') +
                '{:>10}'.format('DATTYP') +
                '{:>10}'.format(' ')+'\n')

        f.write('{:>10d}'.format(5000)+
                '{:>10d}'.format(0) + 
                '{:>10.2f}'.format(1.0) + 
                '{:>10.2f}'.format(1.0) + 
                '{:>10.2f}'.format(0.0) +
                '{:>10.2f}'.format(0.0) +
                '{:>10d}'.format(0) +
                '{:>10d}'.format(0) + '\n')

        f.write('$'+'{:>9}'.format(' ')+
                '{:>10}'.format('A1')+
                '{:>10}'.format(' ')+
                '{:>10}'.format('O1')+'\n')
        for (x, y) in zip(triax, eps):
            f.write('{:>10}'.format(' ')+
                    '{:>10.3f}'.format(x) + 
                    '{:>10}'.format(' ') +
                    '{:>10.3f}'.format(y)+'\n') 
        f.write('*END\n') 

def writeECRITCurve(triax, eps):
    #print(param)
    with open('3000.cur', 'w+') as f:
        f.write('*KEYWORD\n')
        f.write('*DEFINE_CURVE'+'\n')
        f.write('$#Triaxiality vs. Failure Plastic Strain'+'\n')
        f.write('$'+'{:>9}'.format('LCID')+
                '{:>10}'.format('SIDR') + 
                '{:>10}'.format('SCLA') + 
                '{:>10}'.format('SCLO') + 
                '{:>10}'.format('OFFA') +
                '{:>10}'.format('OFFO') +
                '{:>10}'.format('DATTYP') +
                '{:>10}'.format(' ')+'\n')

        f.write('{:>10d}'.format(3000)+
                '{:>10d}'.format(0) + 
                '{:>10.2f}'.format(1.0) + 
                '{:>10.2f}'.format(1.0) + 
                '{:>10.2f}'.format(0.0) +
                '{:>10.2f}'.format(0.0) +
                '{:>10d}'.format(0) +
                '{:>10d}'.format(0) + '\n')

        f.write('$'+'{:>9}'.format(' ')+
                '{:>10}'.format('A1')+
                '{:>10}'.format(' ')+
                '{:>10}'.format('O1')+'\n')
        for (x, y) in zip(triax, eps):
            f.write('{:>10}'.format(' ')+
                    '{:>10.3f}'.format(x) + 
                    '{:>10}'.format(' ') +
                    '{:>10.3f}'.format(y)+'\n') 
        f.write('*END\n') 


triax = np.arange(-0.66, 0.68, 0.03)

writeSDGCurve(triax, eps_f(triax, lode_b(lode_p(triax))))
writeECRITCurve(triax, eps_i(triax))
print("N o r m a l")