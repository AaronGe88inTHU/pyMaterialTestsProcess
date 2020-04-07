#$
import sys
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
# import warnings
# warnings.filterwarnings('error')
# C = float('<<c>>')
# D = float('<<d>>')
# E = float('<<e>>')
# F = float('<<f>>')
# G = float('<<g>>')

def simplifiedMMC(eta, thetaBar, param):
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
        idx = np.isnan(epsilonPlasticFailure)
        epsilonPlasticFailure[idx] = 2
        #print(epsilonPlasticFailure)
    except RuntimeWarning as e:
        #epsilonPlasticFailure = np.zeros(comp.shape)
        pass
        
       
    return epsilonPlasticFailure
    
def MMCSurface(*param):
    eta = np.arange(-1., 1.1, 0.1)
    theta = np.arange(-1, 1.1, 0.1)
    
    etaX, thetaY = np.meshgrid(eta, theta, sparse=False)
    #z = np.sin(xx**2 + yy**2) / (xx**2 + yy**2)
    #h = plt.contourf(x,y,z)
    epsilon = simplifiedMMC(etaX, thetaY, param)
    '''
        lsdyna has different defination of lode parameter than mmc,
        transfer mmc model to lsdyna format
    '''
    return etaX, thetaY, epsilon

def QuadCurve(*param):
    A, h, k  = param
    theta = np.arange(-1, 1.1, 0.1)
    ercit = A * np.power(theta - h, 2) + k
    
    return theta, ercit
    
def writeTable(failueSurface):
    etaX, thetaY, strain = failueSurface
    #print (etaX, thetaY)
    eta = etaX[0, :]
    theta = np.cos(np.pi / 2 * (1 -  thetaY[:, 0]))
    
    #print(eta.shape, strain.shape)
    with open ('mmc.tab','w+') as f:
        f.write('*KEYWORD\n')
        f.write("$#TABLE for MMC model\n") 
        f.write('*DEFINE_TABLE\n')
        f.write('$#Lode Parameter vs. load curves'+'\n')
        f.write('$'+'{:>9}'.format('TBID')+'\n')
        f.write(' '+'{:>9d}'.format(5000)+'\n')
        f.write('$'+'{:>9}'.format(' ')+
            '{:>10}'.format('VALUE')+
            '{:>10}'.format('LCID')+'\n')
        
        for ii, ll in enumerate(theta):
            #print(ii)
            f.write('{:>10}'.format(' ')+
                '{:>10.3f}'.format(ll)+
                '{:10d}'.format(ii+5001)+'\n')
        f.write('$'+'\n')
        
        for ii, _ in enumerate(theta):
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

            f.write('{:>10d}'.format(ii+5001)+
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
            for jj, tt in enumerate(eta):
                f.write('{:>10}'.format(' ')+
                    '{:>10.3f}'.format(tt) + 
                    '{:>10}'.format(' ') +
                    '{:>10.2e}'.format(strain[ii,jj])+'\n')
                    
def writeErcit(theta, ercit):
    with open ('mmc.tab','a+') as f:
        f.write('*KEYWORD\n')
        f.write("$#TABLE for MMC model\n") 
        f.write('*DEFINE_CURVE\n')
        f.write('$#Lode Parameter vs. load curves'+'\n')
        f.write('$'+'{:>9}'.format('TBID')+'\n')
        f.write(' '+'{:>9d}'.format(3000)+'\n')
        f.write('$'+'{:>9}'.format(' ')+
            '{:>10}'.format('VALUE')+
            '{:>10}'.format('LCID')+'\n')

        for t, eps in zip(theta, ercit):
            f.write('{:>10}'.format(' ')+
                    '{:>10.3f}'.format(t) + 
                    '{:>10}'.format(' ') +
                    '{:>10.2e}'.format(eps)+'\n')
        f.write('*END')

def writeParameter(param):
    eps_s1, eps_s2, eps_t, eps_n, eps_p = param
    with open('gissimo.cur', 'w+') as f:
        f.write('*KEYWORD\n')
        f.write('*PARAMETER\n')
        f.write('$#\n')
        f.write('{:<10}'.format('reps_s1'))
        f.write('{:<10.3f}'.format(eps_s1)+'\n')
        f.write('{:<10}'.format('reps_s2'))
        f.write('{:<10.3f}'.format(eps_s2)+'\n')
        f.write('{:<10}'.format('reps_t'))
        f.write('{:<10.3f}'.format(eps_t)+'\n')
        f.write('{:<10}'.format('reps_n'))
        f.write('{:<10.3f}'.format(eps_n)+'\n')
        f.write('{:<10}'.format('reps_p'))
        f.write('{:<10.3f}'.format(eps_p)+'\n')
        

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

        f.write('{:>10}'.format('')+
                '{:>10}'.format(-0.2)+
                '{:>10}'.format(' ')+
                '{:>10.3f}'.format(2) +'\n')

        f.write('{:>10}'.format('')+
                '{:>10.5f}'.format(-0.1)+
                '{:<10}'.format('&eps_s1') +'\n')
        f.write('{:>10}'.format('')+
                '{:>10.5f}'.format(0.1)+
                '{:<10}'.format('&eps_s2') +'\n')
        f.write('{:>10}'.format('')+
                '{:>10.5f}'.format(0.33333)+
                '{:<10}'.format('&eps_t') +'\n')
        f.write('{:>10}'.format('')+
                '{:>10.5f}'.format(0.577)+
                '{:<10}'.format('&eps_n') +'\n')
        f.write('{:>10}'.format('')+
                '{:>10.5f}'.format(0.6666)+
                '{:<10}'.format('&eps_p') +'\n')
                    
        f.write('*END')

writeParameter([0,0,0,0,0])

