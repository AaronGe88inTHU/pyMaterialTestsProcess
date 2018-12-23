import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
def DamageInitial(Ts, rs):
    def f0(x):
        d1, d2, d3 = x
        return rs[0] - (d1 + d2* np.exp(-d3*Ts[0]))

    def f1(x):
        d1, d2, d3 = x
        return rs[1] - (d1 + d2* np.exp(-d3*Ts[1]))
    
    def f2(x):
        d1, d2, d3 = x
        return rs[2] - (d1 + d2* np.exp(-d3*Ts[2]))

    def fun(x):
        return [f0(x), f1(x), f2(x)]
    
    plt.plot(Ts, rs)
    
    result = fsolve(fun, [1,1,1])
    
    curve = result[0] + result[1] * np.exp(-result[2] * np.arange(0, 1.8, 0.1))
    #print(curve)
    plt.plot(np.arange(0, 1.8, 0.1), curve)

    plt.show()
    print(result)
    return result

def DamageFailure(Ts, rf, d3):
    def f0(x):
        d1, d2 = x
        return rf[0] - (d1 + d2* np.exp(-d3*Ts[0]))

    def f1(x):
        d1, d2 = x
        return rf[1] - (d1 + d2* np.exp(-d3*Ts[1]))


    def fun(x):
        return [f0(x), f1(x)]
    
    plt.plot(Ts, rf)
    
    result = fsolve(fun, [1,1])
    
    curve = result[0] + result[1] * np.exp(-d3 * np.arange(0, 1.8, 0.1))
    #print(curve)
    plt.plot(np.arange(0, 1.8, 0.1), curve)

    plt.show()
    print(result)

init = DamageInitial([0, 0.33, 1.0], [0.234, 0.11, 0.059])
DamageFailure([0, 1.0],[0.448, 0.065], init[2])