import sys
import logging
from FileOperate import readXlsx
import Paramters
from FitModel import fitModel
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
def showFigure(faiureSurface):
    XX, YY, zz = faiureSurface
    fig = plt.figure()
    #plt.xlabel('Triaxiality')
    #plt.ylabel('Lode Parameter')
    #plt.zlabel('Failure plastic strain')
    ax = fig.gca(projection='3d')
    #cs = ax.contourf(X, Y, z, locator=ticker.LogLocator(), cmap=cm.PuBu_r)
    #cbar = fig.colorbar(cs)
    ax.plot_surface(XX, YY, zz, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
    ax.xaxis.set_major_locator(LinearLocator(5))
    ax.yaxis.set_major_locator(LinearLocator(5))
    ax.set_xlabel('Triaxiality')
    ax.set_ylabel('Lode Parameter')
    ax.set_zlabel('Failure plastic strain')
    #ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f')
    plt.show()

def writeTable(failueSurface):
    etaX, thetaY, strain = failueSurface
    #print (etaX, thetaY)
    eta = etaX[0, :]
    theta = thetaY[:, 0]
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
        
def main(argv):
    _, fileName, A, n = argv
    Paramters.A = float(A)
    Paramters.n = float(n)
    tests = readXlsx(fileName)
    c1, c2 = fitModel(tests)
    failureSurface = MMCSurface(Paramters.A, Paramters.n, c1, c2)
    writeTable(failureSurface)
    showFigure(failureSurface)

    
    

if __name__ == "__main__":
    main(sys.argv)