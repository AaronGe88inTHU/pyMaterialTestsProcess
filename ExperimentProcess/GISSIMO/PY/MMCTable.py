#$
import sys
import numpy as np
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
        print(epsilonPlasticFailure)
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
    
A = 3043.18303
n = 0.12954
# C, D = -2, 1000
# E, F, G = 1, -1, 1
failureSurface = MMCSurface(A, n, np.exp(C), D)

# import matplotlib.pyplot as plt
# from matplotlib import ticker, cm
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.ticker import LinearLocator, FormatStrFormatter

# def showFigure(faiureSurface, tests):
    # XX, YY, zz = faiureSurface
    # fig = plt.figure()
    # #plt.xlabel('Triaxiality')
    # #plt.ylabel('Lode Parameter')
    # #plt.zlabel('Failure plastic strain')
    # ax = fig.gca(projection='3d')
    # #cs = ax.contourf(X, Y, z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)
    # #cbar = fig.colorbar(cs)
    
    # ax.scatter3D(XX, YY, zz, cmap=cm.coolwarm,
                       # linewidth=0, antialiased=False)
    # #for test in tests:
    # '''
    # lsdyna has different defination of lode parameter than mmc,
    # transfer mmc model to lsdyna format
    # '''
    # #xx, yy, zz = tests[:, 0], tests[:, 1], tests[:, 2]
    # #ax.scatter(xx, yy, zz)#, cmap=cm.coolwarm,linewidth=0, antialiased=False)
 
    # ax.xaxis.set_major_locator(LinearLocator(5))
    # ax.yaxis.set_major_locator(LinearLocator(5))
    # ax.set_xlabel('Triaxiality')
    # ax.set_ylabel('Lode Parameter')
    # ax.set_zlabel('Failure plastic strain')
    # ax.set_zbound([0,1.5])
    # #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f')
    # plt.show()
# showFigure(failureSurface,[])

writeTable(failureSurface)
eta, ercit = QuadCurve(E, F, G)
writeErcit(eta, ercit)
print("N o r m a l")
