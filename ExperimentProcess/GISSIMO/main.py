import sys
import logging
from FileOperate import readXlsx
import Paramters
from FitModel import *
from GISSIMO import MMCSurface
import matplotlib.pyplot as plt
from matplotlib import ticker, cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')

def planeStressMMC(model, param):
    tris = []
    lps = []
    for sigma1 in np.arange(-0.5, -0.1, 0.1):
        sigma2 = -0.5
        while True:
            pressure = (sigma2 + sigma1) / 3
            mises = np.sqrt(((sigma1-sigma2) ** 2 + sigma2 ** 2 + sigma1 ** 2)/2)
            tri = pressure / mises
            lp = (2 * sigma2 - sigma1) / sigma1
            tris .append(tri)
            lps.append(lp)
            sigma2 = sigma2 + 0.1
            if(sigma2 > sigma1):
                break
    
    #print(triLp.shape)
    strain = model(np.array(tris), np.array(lps), param)
    #print(strain.shape)
    print(tris)
    return np.array(tris).reshape(-1,1),  np.array(lps).reshape(-1,1), strain.reshape(-1,1)
#line = planeStressMMC(simplifiedMMC, resAcc)


def showFigure(faiureSurface, tests, line):
    XX, YY, ZZ = faiureSurface
    fig = plt.figure()
    #plt.xlabel('Triaxiality')
    #plt.ylabel('Lode Parameter')
    #plt.zlabel('Failure plastic strain')
    ax = fig.gca(projection='3d')
    #cs = ax.contourf(X, Y, z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)
    #cbar = fig.colorbar(cs)
    ax.plot_surface(XX, YY, ZZ, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False, alpha=0.5)
    #for test in tests:
    #    x, y, z = test[:, 0], test[:, 1], test[:, 2]
    #    ax.plot(x, y, z)#, cmap=cm.coolwarm,linewidth=0, antialiased=False)
    #cset = ax.contour(XX, YY, ZZ, zdir='y',map=cm.coolwarm)
    #print(line)
    #print(line[0].shape)
    #ax.plot(line[0][:,0], line[1][:, 0], line[2][:, 0])
    ax.xaxis.set_major_locator(LinearLocator(5))
    ax.yaxis.set_major_locator(LinearLocator(5))
    ax.set_xlabel('Triaxiality')
    ax.set_ylabel('Lode Parameter')
    ax.set_zlabel('Failure plastic strain')
    ax.set_zbound([0,1.5])
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f')

    plt.show()



def writeTable(failueSurface):
    etaX, thetaY, strain = failueSurface
    #print (etaX, thetaY)
    eta = etaX[0, :]
    theta = thetaY[:, 0]
    print(eta.shape, theta.shape)
    with open ('mmc.tab','w+') as f:
        
        f.write('*DEFINE_TABLE\n')
        f.write('$'+'{:>9}'.format('TBID')+'\n')
        f.write(' '+'{:>9d}'.format(eta.shape[0]+1)+'\n')
        f.write('$'+'{:>9}'.format(' ')+
            '{:>10}'.format('VALUE')+
            '{:>10}'.format('LCID')+'\n')
        for ii, ll in enumerate(theta):
            #print(ii)
            f.write('{:>10}'.format(' ')+
                '{:>10.3f}'.format(ll)+
                '{:10d}'.format(ii+1)+'\n')
        f.write('$'+'\n')
        for ii, _ in enumerate(eta):
            f.write('*DEFINE_CURVE'+'\n')
            f.write('$'+'{:>9}'.format('LCID')+
                '{:>10}'.format('SIDR') + 
                '{:>10}'.format('SCLA') + 
                '{:>10}'.format('SCLO') + 
                '{:>10}'.format('OFFA') +
                '{:>10}'.format('OFFO') +
                '{:>10}'.format('DATTYP') +
                '{:>10}'.format(' ')+'\n')

            f.write('{:>10d}'.format(ii+1)+
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
            for jj, tt in enumerate(theta):
                f.write('{:>10}'.format(' ')+
                    '{:>10.3f}'.format(tt) + 
                    '{:>10}'.format(' ') +
                    '{:>10.2e}'.format(strain[jj,ii])+'\n')
        
def main():#argv):
    tests = readXlsx('clearedData.xlsx')

    resUsingFractureStrain = fitModelUsingFractureStrain(tests)
    #resUsingFractureStrain
    resAcc = fitDamageAcc(tests, resUsingFractureStrain.x)
    #resAcc
    a, b , c, d = resAcc.x[:]
    failureSurface = MMCSurface(a, b, c,d)
    line = planeStressMMC(simplifiedMMC, (a, b, c, d))
    #print(line.shape)
    showFigure(failureSurface, tests, line)
    writeTable(failureSurface)

    

#if __name__ == "__main__":
main()